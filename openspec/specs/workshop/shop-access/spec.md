# workshop/shop-access Specification

## Purpose
Defines how everything in this repository reaches the demo shop - locally by default, on the shared instance as a fallback - so that every participant's state stays their own and one setting change moves all tools at once.

## Requirements

### Requirement: Shop from one pinned image
The repository SHALL run the shop only from the published demo-webshop image, referenced by a single version tag in exactly one place. It MUST NOT reference the `edge` tag or any `sha-` tag, and MUST NOT build the shop.

#### Scenario: Changing the pinned tag
- **WHEN** the tag is changed in its one location and the local shop is started again
- **THEN** the shop's health check reports the new version

#### Scenario: No floating references
- **WHEN** the repository is searched for references to the shop image
- **THEN** every reference resolves to the one pinned version tag

### Requirement: Local shop by default
With no configuration, the documented start command SHALL make the shop reachable at `http://localhost:9090`, and the documented reset command SHALL return it to a freshly seeded state.

#### Scenario: First start
- **WHEN** a participant runs the start command without any configuration
- **THEN** the shop answers its health check at `http://localhost:9090` with the pinned version

#### Scenario: Reset to a known state
- **WHEN** a participant has placed orders and changed presets and then runs the reset command
- **THEN** the shop has no runtime orders and renders the clean state

### Requirement: One configuration contract
The shop URL and the workshop space SHALL be selected by exactly two settings, `SHOP_URL` and `SHOP_SPACE`, read from the process environment or from a git-ignored `.env` file in the repository root, with the process environment taking precedence. Without either setting, tools SHALL use the local shop and no space. Every tool in the repository that talks to the shop MUST honour both settings identically.

#### Scenario: Settings from the .env file
- **WHEN** `.env` sets `SHOP_URL` and `SHOP_SPACE` and neither is set in the environment
- **THEN** the test run and the shop helper both use that URL and that space

#### Scenario: Environment wins
- **WHEN** `SHOP_SPACE` is set both in `.env` and in the process environment
- **THEN** the value from the process environment is used

### Requirement: Shared instance as the fallback
Setting `SHOP_URL` to the shared instance and `SHOP_SPACE` to the participant's GitHub handle SHALL be sufficient to run every lab against the shared instance, with that participant's presets, carts and orders confined to their space.

#### Scenario: Two participants, two presets
- **WHEN** two participants apply different presets in their own spaces on the shared instance
- **THEN** each of them sees only the preset they applied

### Requirement: The space travels with every request
When `SHOP_SPACE` is set, every request that a tool of this repository sends to the shop - page loads, assets and API calls alike - SHALL carry that space.

#### Scenario: A page opened in shared mode
- **WHEN** a repository tool opens a shop page with `SHOP_SPACE` set to `octocat`
- **THEN** the page reports `octocat` as its workshop space

### Requirement: Run profiles
The documented test run command SHALL offer a `local` and a `shared` profile, selectable with a single option. Running without a profile SHALL behave as `local`. The `shared` profile SHALL default the shop URL to the shared instance and SHALL require a space.

#### Scenario: Shared profile without a space
- **WHEN** a participant runs the suite with the `shared` profile and no space configured
- **THEN** the run stops before the first test and explains how to set the space

### Requirement: Shop helper
The repository SHALL provide a helper command that works identically in both modes and can: show the shop's status; list the presets; apply a named preset in the current space; reset the current space; and wait until the shop is healthy. The status SHALL report the shop version, the space, and every preset whose settings all hold in the space - presets are partial and compose, so several can hold at once - or `custom` when none holds. It MUST NOT list individual planted-bug flags.

#### Scenario: Applying a preset
- **WHEN** a participant applies preset `stage2` with the helper
- **THEN** the status afterwards names `stage2` among the presets that hold

#### Scenario: Composed presets
- **WHEN** a participant applies `stage2` and then `buggy`
- **THEN** the status names both `stage2` and `buggy`

#### Scenario: Status stays neutral
- **WHEN** preset `buggy` is active and the participant asks for the status
- **THEN** the status names `buggy` and does not name any individual bug flag

### Requirement: The shared default space is never written
On the shared instance, the helper SHALL refuse to apply a preset or reset without a configured space, and SHALL explain how to set one, instead of sending the request.

#### Scenario: Preset without a space on the shared instance
- **WHEN** `SHOP_URL` points at the shared instance, no space is configured, and a preset is requested
- **THEN** the helper sends no request and explains how to set `SHOP_SPACE`
