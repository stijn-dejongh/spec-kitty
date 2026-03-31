# SSH Deploy Key Setup for CI/CD

## Purpose

Spec Kitty depends on the private `spec-kitty-events` library. GitHub Actions
needs an SSH deploy key to clone that repository during CI and release flows.

## Setup

### 1. Generate a key pair

```bash
ssh-keygen -t ed25519 -C "spec-kitty-ci-deploy-key" -f spec-kitty-events-deploy-key -N ""
```

This creates:

- `spec-kitty-events-deploy-key` — private key for GitHub Actions secret
- `spec-kitty-events-deploy-key.pub` — public key for the private dependency repo

### 2. Add the public key to `spec-kitty-events`

1. Open `https://github.com/Priivacy-ai/spec-kitty-events/settings/keys`
2. Click `Add deploy key`
3. Title: `spec-kitty CI/CD Read-Only`
4. Paste the contents of `spec-kitty-events-deploy-key.pub`
5. Leave write access disabled

### 3. Add the private key to this repository

1. Open `https://github.com/Priivacy-ai/spec-kitty/settings/secrets/actions`
2. Create a repository secret named `SPEC_KITTY_EVENTS_DEPLOY_KEY`
3. Paste the full contents of `spec-kitty-events-deploy-key`

### 4. Remove the local key files

```bash
rm spec-kitty-events-deploy-key spec-kitty-events-deploy-key.pub
```

## Verification

Trigger a workflow run that needs the private dependency and verify the clone
step succeeds.

## Troubleshooting

### `Permission denied (publickey)`

- confirm the public key was added to `spec-kitty-events`
- confirm the secret name is exactly `SPEC_KITTY_EVENTS_DEPLOY_KEY`

### `Could not read from remote repository`

- confirm the dependency uses an SSH Git URL
- confirm the deploy key has read access to `spec-kitty-events`

## Rotation

Rotate the key at least every 12 months, or immediately if it may be
compromised.
