package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

const (
	settingsPath = ".claude/settings.json"
)

var (
	titleStyle = lipgloss.NewStyle().
			MarginLeft(2).
			Foreground(lipgloss.Color("#7D56F4")).
			Bold(true)

	itemStyle = lipgloss.NewStyle().
			PaddingLeft(4)

	selectedItemStyle = lipgloss.NewStyle().
				PaddingLeft(2).
				Foreground(lipgloss.Color("#7D56F4")).
				Bold(true)

	descStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#626262")).
			MarginLeft(2)

	successStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#04B575")).
			Bold(true)

	errorStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FF0000")).
			Bold(true)
)

// SoundSuite represents a collection of themed sounds
type SoundSuite struct {
	Name        string
	Desc        string
	Path        string
	PreviewFile string
}

func (s SoundSuite) Title() string       { return s.Name }
func (s SoundSuite) Description() string { return s.Desc }
func (s SoundSuite) FilterValue() string { return s.Name }

// Model represents the application state
type model struct {
	list            list.Model
	suites          []SoundSuite
	audioPlayer     string
	repoPath        string
	choice          string
	quitting        bool
	confirming      bool
	selectedSuite   *SoundSuite
	err             error
	success         bool
	lastPreview     string
	previewCooldown time.Time
}

// Hook types we manage (sound-related only)
var soundHooks = []string{
	"session_start",
	"session_end",
	"tool_start",
	"tool_complete",
	"prompt_submit",
	"response_start",
	"response_end",
	"subagent_done",
	"precompact_warning",
	"notification",
}

func main() {
	// Get repository path (where this binary is run from)
	repoPath, err := os.Getwd()
	if err != nil {
		fmt.Printf("Error getting current directory: %v\n", err)
		os.Exit(1)
	}

	// Detect audio player
	audioPlayer := detectAudioPlayer()
	if audioPlayer == "" {
		fmt.Println("❌ No audio player found (tried: afplay, paplay, aplay)")
		fmt.Println("Please install one of the following:")
		fmt.Println("  - macOS: afplay (built-in)")
		fmt.Println("  - Linux: aplay (alsa-utils) or paplay (pulseaudio-utils)")
		os.Exit(1)
	}

	// Scan for sound suites
	suites := scanSoundSuites(repoPath)
	if len(suites) == 0 {
		fmt.Println("❌ No sound suites found in repository")
		os.Exit(1)
	}

	// Create list items
	items := make([]list.Item, len(suites))
	for i, suite := range suites {
		items[i] = suite
	}

	// Create list
	const defaultWidth = 80
	const listHeight = 14

	l := list.New(items, list.NewDefaultDelegate(), defaultWidth, listHeight)
	l.Title = "🎵 Claude Code Sounds Configurator"
	l.SetShowStatusBar(false)
	l.SetFilteringEnabled(false)
	l.Styles.Title = titleStyle

	// Create model
	m := model{
		list:        l,
		suites:      suites,
		audioPlayer: audioPlayer,
		repoPath:    repoPath,
	}

	// Run program
	p := tea.NewProgram(m, tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.list.SetWidth(msg.Width)
		return m, nil

	case tea.KeyMsg:
		// Handle confirmation mode
		if m.confirming {
			switch keypress := msg.String(); keypress {
			case "y", "Y":
				// User confirmed, apply the configuration
				if m.selectedSuite != nil {
					m.choice = m.selectedSuite.Name
					err := m.applyConfiguration(*m.selectedSuite)
					if err != nil {
						m.err = err
						m.success = false
					} else {
						m.success = true
					}
					m.quitting = true
					return m, tea.Quit
				}
			case "n", "N", "esc":
				// User cancelled, go back to list
				m.confirming = false
				m.selectedSuite = nil
				return m, nil
			}
			return m, nil
		}

		// Normal mode
		switch keypress := msg.String(); keypress {
		case "ctrl+c", "q":
			m.quitting = true
			return m, tea.Quit

		case "enter":
			// Enter confirmation mode
			i, ok := m.list.SelectedItem().(SoundSuite)
			if ok {
				m.confirming = true
				suite := i // Make a copy
				m.selectedSuite = &suite
				return m, nil
			}

		case "p", " ":
			// Preview sound on 'p' or spacebar
			i, ok := m.list.SelectedItem().(SoundSuite)
			if ok && time.Now().After(m.previewCooldown) {
				m.lastPreview = i.Name
				m.previewCooldown = time.Now().Add(1 * time.Second)
				go m.playPreview(i)
			}
		}

	}

	var cmd tea.Cmd
	m.list, cmd = m.list.Update(msg)
	return m, cmd
}

func (m model) View() string {
	if m.quitting {
		if m.err != nil {
			return errorStyle.Render(fmt.Sprintf("\n❌ Error: %v\n", m.err))
		}
		if m.success {
			return successStyle.Render(fmt.Sprintf("\n✅ Successfully configured '%s' theme!\n", m.choice)) +
				descStyle.Render("\nYour settings have been updated at ~/.claude/settings.json\n") +
				descStyle.Render("A backup was created with timestamp.\n\n")
		}
		return "\nGoodbye!\n"
	}

	// Show confirmation dialog
	if m.confirming && m.selectedSuite != nil {
		confirmStyle := lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#7D56F4")).
			Padding(1, 2).
			MarginTop(2).
			MarginLeft(2)

		confirmTitle := titleStyle.Render("💾 Confirm Theme Change")
		confirmMsg := fmt.Sprintf("\nApply '%s' theme?\n", m.selectedSuite.Name)
		confirmDesc := descStyle.Render(fmt.Sprintf("  %s\n", m.selectedSuite.Desc))
		confirmActions := "\n  This will:\n" +
			"  • Create a backup of your current settings\n" +
			"  • Update all 10 sound hooks\n" +
			"  • Preserve your other custom hooks\n\n"
		confirmPrompt := successStyle.Render("  Press Y to save and apply") + " • " +
			errorStyle.Render("N or ESC to cancel") + "\n"

		confirmBox := confirmStyle.Render(
			confirmTitle + confirmMsg + confirmDesc + confirmActions + confirmPrompt,
		)

		return "\n" + confirmBox + "\n"
	}

	// Normal list view
	help := descStyle.Render("\n  ↑/↓: navigate  •  enter: select  •  p/space: preview  •  q: quit\n")
	player := descStyle.Render(fmt.Sprintf("  Audio player: %s\n", m.audioPlayer))

	preview := ""
	if m.lastPreview != "" {
		preview = descStyle.Render(fmt.Sprintf("  🔊 Previewing: %s\n", m.lastPreview))
	}

	return "\n" + m.list.View() + help + player + preview
}

// detectAudioPlayer finds an available audio player on the system
func detectAudioPlayer() string {
	players := []string{"afplay", "paplay", "aplay"}

	for _, player := range players {
		if _, err := exec.LookPath(player); err == nil {
			return player
		}
	}

	return ""
}

// scanSoundSuites finds all available sound suites in the repository
func scanSoundSuites(repoPath string) []SoundSuite {
	suites := []SoundSuite{
		{
			Name:        "Terminal Native (Default)",
			Desc:        "Original cyberpunk terminal aesthetic - warm and welcoming",
			Path:        repoPath,
			PreviewFile: "session_start.wav",
		},
		{
			Name:        "Cyberpunk Intense",
			Desc:        "Enhanced digital grit with aggressive terminal energy",
			Path:        filepath.Join(repoPath, "prompt3style"),
			PreviewFile: "session_start.wav",
		},
		{
			Name:        "Retro Terminal",
			Desc:        "Classic 80s computing with clean sine waves and nostalgia",
			Path:        filepath.Join(repoPath, "retro-terminal"),
			PreviewFile: "session_start.wav",
		},
		{
			Name:        "Drift",
			Desc:        "Ambient water soundscape for deep focus and flow state",
			Path:        filepath.Join(repoPath, "drift"),
			PreviewFile: "session_start.wav",
		},
		{
			Name:        "Void",
			Desc:        "Cosmic liminal space with deep drones and stellar resonance",
			Path:        filepath.Join(repoPath, "void"),
			PreviewFile: "session_start.wav",
		},
	}

	// Filter to only existing suites
	var available []SoundSuite
	for _, suite := range suites {
		previewPath := filepath.Join(suite.Path, suite.PreviewFile)
		if _, err := os.Stat(previewPath); err == nil {
			available = append(available, suite)
		}
	}

	return available
}

// playPreview plays a preview sound from the suite
func (m *model) playPreview(suite SoundSuite) {
	previewPath := filepath.Join(suite.Path, suite.PreviewFile)
	cmd := exec.Command(m.audioPlayer, previewPath)
	cmd.Start()
	// Don't wait for completion, let it play in background
}

// applyConfiguration updates the Claude Code settings with the selected sound suite
func (m *model) applyConfiguration(suite SoundSuite) error {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return fmt.Errorf("failed to get home directory: %w", err)
	}

	settingsFile := filepath.Join(homeDir, settingsPath)

	// Create backup
	if err := m.backupSettings(settingsFile); err != nil {
		return fmt.Errorf("failed to create backup: %w", err)
	}

	// Read existing settings
	existingSettings := make(map[string]interface{})
	if data, err := os.ReadFile(settingsFile); err == nil {
		// File exists, parse it
		if err := json.Unmarshal(data, &existingSettings); err != nil {
			return fmt.Errorf("failed to parse existing settings: %w", err)
		}
	}

	// Generate new sound hooks
	newSoundHooks := m.generateHooks(suite)

	// Merge hooks carefully
	existingHooks, ok := existingSettings["hooks"].(map[string]interface{})
	if !ok {
		existingHooks = make(map[string]interface{})
	}

	// Remove old sound hooks, keep everything else
	for _, hookName := range soundHooks {
		delete(existingHooks, hookName)
	}

	// Add new sound hooks
	for hookName, hookValue := range newSoundHooks {
		existingHooks[hookName] = hookValue
	}

	// Update settings
	existingSettings["hooks"] = existingHooks

	// Write back
	data, err := json.MarshalIndent(existingSettings, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal settings: %w", err)
	}

	// Ensure directory exists
	settingsDir := filepath.Dir(settingsFile)
	if err := os.MkdirAll(settingsDir, 0755); err != nil {
		return fmt.Errorf("failed to create settings directory: %w", err)
	}

	// Write file
	if err := os.WriteFile(settingsFile, data, 0644); err != nil {
		return fmt.Errorf("failed to write settings: %w", err)
	}

	return nil
}

// backupSettings creates a timestamped backup of the settings file
func (m *model) backupSettings(settingsFile string) error {
	// Check if file exists
	if _, err := os.Stat(settingsFile); os.IsNotExist(err) {
		// No existing file, no backup needed
		return nil
	}

	// Create backup filename with timestamp
	timestamp := time.Now().Format("20060102_150405")
	backupFile := settingsFile + ".backup_" + timestamp

	// Copy file
	source, err := os.Open(settingsFile)
	if err != nil {
		return err
	}
	defer source.Close()

	destination, err := os.Create(backupFile)
	if err != nil {
		return err
	}
	defer destination.Close()

	_, err = io.Copy(destination, source)
	return err
}

// generateHooks creates the hooks configuration for a sound suite
func (m *model) generateHooks(suite SoundSuite) map[string]interface{} {
	hooks := make(map[string]interface{})

	// Determine if we're on Windows for path formatting
	isWindows := runtime.GOOS == "windows"

	for _, hookName := range soundHooks {
		soundFile := filepath.Join(suite.Path, hookName+".wav")

		// Format path for shell
		if isWindows {
			soundFile = strings.ReplaceAll(soundFile, "/", "\\")
		}

		// Build command
		var command string
		if isWindows {
			command = fmt.Sprintf("powershell -c (New-Object Media.SoundPlayer '%s').PlaySync();", soundFile)
		} else {
			// Unix-like systems
			command = fmt.Sprintf("%s %s &", m.audioPlayer, soundFile)
		}

		hooks[hookName] = map[string]string{
			"command":     command,
			"description": getHookDescription(hookName),
		}
	}

	return hooks
}

// getHookDescription returns a human-readable description for each hook
func getHookDescription(hookName string) string {
	descriptions := map[string]string{
		"session_start":      "Plays when a Claude Code session starts",
		"session_end":        "Plays when a Claude Code session ends",
		"tool_start":         "Plays when a tool begins execution",
		"tool_complete":      "Plays when a tool finishes execution",
		"prompt_submit":      "Plays when user submits a prompt",
		"response_start":     "Plays when Claude starts responding",
		"response_end":       "Plays when Claude finishes responding",
		"subagent_done":      "Plays when a subagent completes its task",
		"precompact_warning": "Plays before context window compaction",
		"notification":       "General notification sound",
	}

	if desc, ok := descriptions[hookName]; ok {
		return desc
	}
	return ""
}
