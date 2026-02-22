"""Migration tests for schemas.py AgentProfile re-export.

Verifies that the shallow ``AgentProfile`` class that previously lived in
``specify_cli.constitution.schemas`` has been replaced with a re-export of
the rich doctrine model, and that ``AgentEntry`` is now the correct name for
the lightweight agents.yaml config entry.
"""



class TestAgentProfileReExport:
    """AgentProfile from schemas is the canonical doctrine model."""

    def test_import_from_schemas_works(self):
        """Re-exporting AgentProfile from schemas does not raise."""
        from specify_cli.constitution.schemas import AgentProfile  # noqa: F401

    def test_same_class_as_doctrine_model(self):
        """``schemas.AgentProfile`` IS ``doctrine.agent_profiles.profile.AgentProfile``."""
        from specify_cli.constitution.schemas import AgentProfile as SchemasProfile
        from doctrine.agent_profiles.profile import AgentProfile as DoctrineProfile

        assert SchemasProfile is DoctrineProfile

    def test_rich_model_fields_accessible(self):
        """The re-exported AgentProfile exposes rich model fields (not agent_key)."""
        from specify_cli.constitution.schemas import AgentProfile

        # Rich model has profile_id, not agent_key
        profile = AgentProfile(
            **{
                "profile-id": "migration-test-agent",
                "name": "Migration Test Agent",
                "purpose": "Verify the re-export works correctly",
                "specialization": {"primary-focus": "Testing migration"},
            }
        )
        assert profile.profile_id == "migration-test-agent"
        assert not hasattr(profile, "agent_key")

    def test_agent_entry_still_importable(self):
        """``AgentEntry`` (the renamed shallow class) is importable from schemas."""
        from specify_cli.constitution.schemas import AgentEntry  # noqa: F401

    def test_agent_entry_has_agent_key(self):
        """``AgentEntry`` retains the ``agent_key`` field for agents.yaml compatibility."""
        from specify_cli.constitution.schemas import AgentEntry

        entry = AgentEntry(agent_key="codex")
        assert entry.agent_key == "codex"
        assert entry.role == "implementer"

    def test_agents_config_profiles_are_agent_entry(self):
        """``AgentsConfig.profiles`` holds ``AgentEntry`` instances."""
        from specify_cli.constitution.schemas import AgentEntry, AgentsConfig

        config = AgentsConfig(
            profiles=[
                AgentEntry(agent_key="claude", role="implementer"),
                AgentEntry(agent_key="codex", role="reviewer"),
            ]
        )
        assert len(config.profiles) == 2
        for entry in config.profiles:
            assert isinstance(entry, AgentEntry)
            assert hasattr(entry, "agent_key")

    def test_agent_profile_and_agent_entry_are_different_classes(self):
        """``AgentProfile`` (rich doctrine) and ``AgentEntry`` (shallow) are different."""
        from specify_cli.constitution.schemas import AgentProfile, AgentEntry

        assert AgentProfile is not AgentEntry
