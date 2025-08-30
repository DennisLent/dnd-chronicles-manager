# Development & Releases

This project uses GitHub Actions to build and publish the Character Creator app for Windows, macOS, and Linux using Tauri. The release workflow runs on tagged commits and uploads platform installers to GitHub Releases.

## How releases are triggered
- Automatic on merge to `main`: when changes land on `main`, the CI creates a tag and kicks off a release run.
  - It uses the version in `apps/character-creator/src-tauri/tauri.conf.json`. If a tag for that version already exists, CI bumps the latest `vX.Y.Z` patch number.
  - The tag push triggers a fresh workflow run that builds and publishes the release.
- Manual via Actions: you can run the “Build & Release (Tauri)” workflow with an explicit `version` input to create a tag like `v0.2.0`.

## Versioning
- App bundle version comes from `apps/character-creator/src-tauri/tauri.conf.json` under `version`.
- Keep tags and the app version in sync. For example, update `tauri.conf.json` to `0.2.0` and tag `v0.2.0`.

## Creating a new release
Option A — Merge to `main` (auto-tag)
1. Ensure the app builds locally: `pnpm install` then `pnpm run -C apps/character-creator tauri:build`.
2. Update `apps/character-creator/src-tauri/tauri.conf.json` `version` to the desired value (e.g., `0.2.0`).
3. Open a PR to `main` and merge it.
4. CI creates or bumps a `vX.Y.Z` tag and triggers a release build.

Option B — Manual tag via Actions
1. Open the Actions tab → “Build & Release (Tauri)”.
2. Click “Run workflow” and set `version` (e.g., `0.2.0` or `v0.2.0`).
3. The workflow creates the tag and a separate run on that tag publishes the release.

## What assets are published
- Windows: `.exe` installer if available (fallback: `.msi`).
- macOS: `.dmg` for Apple Silicon (`-arm64`) and Intel (`-x64`) when both are built. A generic `character-creator-macos.dmg` points to a preferred default.
- Linux: `.AppImage` (x86_64), and if available an ARM64 build.

These are uploaded with stable names used by the docs downloads page:

- `character-creator-windows-x64.exe` (or `.msi` if no `.exe`)
- `character-creator-macos.dmg` (generic default)
- `character-creator-macos-arm64.dmg`
- `character-creator-macos-x64.dmg`
- `character-creator-linux-x86_64.AppImage`
- `character-creator-linux-arm64.AppImage` (if built)

You can always find all variants directly on the Releases page as well.

## Manual runs
- You can also dispatch the workflow manually from the Actions tab to test builds (no release) or push a tag to publish a release.

## Docs integration
- The downloads page links to the stable asset names from the latest Release.
- If you add new platforms or file types, update the workflow’s renaming step and the docs page accordingly.
