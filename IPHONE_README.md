# PAVORA AI CONTROL — iPhone-first
This is the **iPhone Safari gesture lab**. Open the deployed HTTPS page on an iPhone, grant front camera permission, and swipe an open hand to switch demo cards or pinch to select one.

**Limitations:** Controls ONLY this page. iOS does not let a Safari page control the home screen, other apps, Settings, or system touches. No background camera tracking.

Technology: MediaPipe Hand Landmarker (browser JavaScript). Camera frames stay in the browser; the model and library are fetched from their public CDNs. iPhone Safari and camera access need HTTPS plus camera permission.

## Publishing
Project lives at repository root `index.html` in `Max791687/max`. In GitHub:
Settings > Pages > Build and deployment: Deploy from a branch > main > /(root) > Save.
When published, the URL should be `https://max791687.github.io/max/` (only after GitHub Pages successfully deploys).

## Roadmap
1. iPhone browser gesture lab (this version)
2. Safe Shortcuts integration for supported tasks with explicit user confirmation
3. Native iOS companion if broader permitted system capabilities are required
4. Resume Windows desktop controller
