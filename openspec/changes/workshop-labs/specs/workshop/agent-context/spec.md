## RENAMED Requirements

- FROM: `### Requirement: Two spec namespaces`
- TO: `### Requirement: Spec namespaces`

## MODIFIED Requirements

### Requirement: Spec namespaces
The OpenSpec configuration SHALL describe three namespaces: `shop/*` for the behaviour of the shop, which agents use as reference when writing tests; `suite/*` for what a participant's own tests verify, where the changes participants propose in Module 5 write their specs; and `workshop/*` for the guarantees of this repository, which participants' agents do not need. A change that adds or changes tests MUST NOT write to `shop/*` or `workshop/*`.

#### Scenario: Context for a new artifact
- **WHEN** an agent requests the instructions for any OpenSpec artifact
- **THEN** the returned project context explains the three namespaces, which one describes the shop, and which one a change that adds tests writes to

#### Scenario: A participant proposes tests for a story
- **WHEN** a participant proposes a change that automates criteria of a shop story
- **THEN** the change's delta specs are created under `suite/*`, and the main specs under `shop/*` and `workshop/*` are unchanged by its archive
