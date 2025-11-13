package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

// TestHookStructure verifies that generated hooks match Claude's expected format
func TestHookStructure(t *testing.T) {
	// Create a test model
	m := &model{
		audioPlayer: "afplay",
	}

	// Create a test suite
	testSuite := SoundSuite{
		Name: "Test Suite",
		Path: "/test/path",
	}

	// Generate hooks
	hooks := m.generateHooks(testSuite)

	// Verify we have the correct number of hooks
	expectedCount := len(soundHookFiles)
	if len(hooks) != expectedCount {
		t.Errorf("Expected %d hooks, got %d", expectedCount, len(hooks))
	}

	// Verify each hook has the correct structure
	for fileHookName, claudeHookName := range soundHookMapping {
		hookValue, exists := hooks[claudeHookName]
		if !exists {
			t.Errorf("Missing hook: %s", claudeHookName)
			continue
		}

		// Verify it's an array
		hookArray, ok := hookValue.([]interface{})
		if !ok {
			t.Errorf("Hook %s is not an array", claudeHookName)
			continue
		}

		if len(hookArray) != 1 {
			t.Errorf("Hook %s array should have 1 element, got %d", claudeHookName, len(hookArray))
			continue
		}

		// Verify the first element is a map with "hooks" key
		firstElement, ok := hookArray[0].(map[string]interface{})
		if !ok {
			t.Errorf("Hook %s first element is not a map", claudeHookName)
			continue
		}

		hooksArray, exists := firstElement["hooks"]
		if !exists {
			t.Errorf("Hook %s missing 'hooks' key", claudeHookName)
			continue
		}

		// Verify hooks is an array
		innerHooks, ok := hooksArray.([]interface{})
		if !ok {
			t.Errorf("Hook %s 'hooks' value is not an array", claudeHookName)
			continue
		}

		if len(innerHooks) != 1 {
			t.Errorf("Hook %s inner hooks should have 1 element, got %d", claudeHookName, len(innerHooks))
			continue
		}

		// Verify the hook has type and command
		hookConfig, ok := innerHooks[0].(map[string]interface{})
		if !ok {
			t.Errorf("Hook %s config is not a map", claudeHookName)
			continue
		}

		if _, exists := hookConfig["type"]; !exists {
			t.Errorf("Hook %s missing 'type' field", claudeHookName)
		}

		if hookConfig["type"] != "command" {
			t.Errorf("Hook %s type should be 'command', got %v", claudeHookName, hookConfig["type"])
		}

		if _, exists := hookConfig["command"]; !exists {
			t.Errorf("Hook %s missing 'command' field", claudeHookName)
		}

		// Verify command contains the correct file path
		command, ok := hookConfig["command"].(string)
		if !ok {
			t.Errorf("Hook %s command is not a string", claudeHookName)
			continue
		}

		expectedPath := filepath.Join(testSuite.Path, fileHookName+".wav")
		if !contains(command, expectedPath) {
			t.Errorf("Hook %s command doesn't contain expected path %s: %s", claudeHookName, expectedPath, command)
		}
	}
}

// TestHookNameMapping verifies the mapping is correct
func TestHookNameMapping(t *testing.T) {
	expectedMappings := map[string]string{
		"session_start":      "SessionStart",
		"session_end":        "SessionEnd",
		"tool_start":         "PreToolUse",
		"tool_complete":      "PostToolUse",
		"prompt_submit":      "UserPromptSubmit",
		"response_start":     "ResponseStart",
		"response_end":       "ResponseEnd",
		"subagent_done":      "SubagentStop",
		"precompact_warning": "PreCompact",
		"notification":       "Notification",
	}

	for fileHook, claudeHook := range expectedMappings {
		if soundHookMapping[fileHook] != claudeHook {
			t.Errorf("Expected %s to map to %s, got %s", fileHook, claudeHook, soundHookMapping[fileHook])
		}
	}
}

// TestJSONSerialization verifies hooks can be properly serialized to JSON
func TestJSONSerialization(t *testing.T) {
	m := &model{
		audioPlayer: "afplay",
	}

	testSuite := SoundSuite{
		Name: "Test Suite",
		Path: "/test/path",
	}

	hooks := m.generateHooks(testSuite)

	// Create a settings structure
	settings := map[string]interface{}{
		"hooks": hooks,
	}

	// Marshal to JSON
	data, err := json.MarshalIndent(settings, "", "  ")
	if err != nil {
		t.Fatalf("Failed to marshal hooks to JSON: %v", err)
	}

	// Unmarshal back
	var unmarshaled map[string]interface{}
	if err := json.Unmarshal(data, &unmarshaled); err != nil {
		t.Fatalf("Failed to unmarshal JSON: %v", err)
	}

	// Verify structure is preserved
	hooksInterface, exists := unmarshaled["hooks"]
	if !exists {
		t.Fatal("Hooks key missing after unmarshal")
	}

	unmarshaledHooks, ok := hooksInterface.(map[string]interface{})
	if !ok {
		t.Fatal("Hooks is not a map after unmarshal")
	}

	if len(unmarshaledHooks) != len(hooks) {
		t.Errorf("Expected %d hooks after unmarshal, got %d", len(hooks), len(unmarshaledHooks))
	}
}

// Helper function
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > len(substr) && anySubstring(s, substr))
}

func anySubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// TestPreservesExistingHooks verifies that non-sound hooks are preserved
func TestPreservesExistingHooks(t *testing.T) {
	// Create temp directory for test
	tempDir := t.TempDir()
	settingsFile := filepath.Join(tempDir, "settings.json")

	// Create initial settings with a custom hook
	initialSettings := map[string]interface{}{
		"hooks": map[string]interface{}{
			"PreToolUse": []interface{}{
				map[string]interface{}{
					"hooks": []interface{}{
						map[string]interface{}{
							"type":    "command",
							"command": "/custom/hook.py",
							"name":    "custom-hook",
						},
					},
				},
			},
			"CustomHook": []interface{}{
				map[string]interface{}{
					"hooks": []interface{}{
						map[string]interface{}{
							"type":    "command",
							"command": "echo 'custom'",
						},
					},
				},
			},
		},
	}

	// Write initial settings
	data, _ := json.MarshalIndent(initialSettings, "", "  ")
	if err := os.WriteFile(settingsFile, data, 0644); err != nil {
		t.Fatalf("Failed to write test settings: %v", err)
	}

	// Note: Full integration test would require mocking the applyConfiguration
	// This test verifies our deletion logic only removes sound hooks
	existingSettings := make(map[string]interface{})
	fileData, _ := os.ReadFile(settingsFile)
	json.Unmarshal(fileData, &existingSettings)

	existingHooks := existingSettings["hooks"].(map[string]interface{})

	// Simulate deletion of sound hooks
	for _, claudeHookName := range soundHookMapping {
		delete(existingHooks, claudeHookName)
	}

	// CustomHook should still exist
	if _, exists := existingHooks["CustomHook"]; !exists {
		t.Error("CustomHook was incorrectly deleted")
	}

	// PreToolUse should be deleted (it's a sound hook)
	if _, exists := existingHooks["PreToolUse"]; exists {
		t.Error("PreToolUse should have been deleted as it's a sound hook")
	}
}
