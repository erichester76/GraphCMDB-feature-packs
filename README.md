# Feature Packs Store

This repository is a local store for feature packs used by this CMDB.

## Usage
- Configure `FEATURE_PACK_STORE_REPO` and `FEATURE_PACK_STORE_BRANCH` in `core/settings.py`.
- The app will pull the repo on each Feature Packs page load.
- Add a pack to the app via the Feature Packs UI (installs from the store).
- Delete a pack from the app via the Feature Packs UI (removes it from the app, not from the store).

## Notes
- This repo is local by default. Add a remote to publish to GitHub.
