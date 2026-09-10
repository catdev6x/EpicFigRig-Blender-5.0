# The EpicFigRig (Blender 5.0 Edition)

> *"Never gonna give your rig up, never gonna let your bones down."* 

A community patch and update for the popular **EpicFigRig (JabLab Version)** Lego minifigure rigging addon, fully adapted and modernized for **Blender 5.0+** by **@catdev6x**.

---

##  What's New in Version 1.3.2 (Blender 5.0 Update by catdev6x)

###  Blender 5.0 Compatibility & Bug Fixes:
* **Blender 5.0 Bone Selection API:** Migrated bone selection to `PoseBone.select` following the removal of `Bone.select` in Blender 5.0.
* **Hand Detection Fix:** Fixed `UnboundLocalError: cannot access local variable 'handname'` during auto-rigging.
* **Smears Drivers:** Rewrote limb visibility drivers so original meshes hide instantly when `LArmSmear`, `RArmSmear`, `LLegSmear`, or `RLegSmear` are dialed up.
* **New UI Feature — Pivot Body Switch:** Added **Enable / Disable** buttons in the panel to toggle waist edge-pivot constraints for smooth body rotation during dynamic animation (e.g., run cycles).
* **UI Stability:** Fixed `UnboundLocalError: check_prop` and `AttributeError: NoneType` crashes when nothing is selected in the viewport.
* **Container Empty Cleanup:** Fixed the parent condition so imported Mecabricks container empties are cleanly removed upon rigging.
* **Snapping Fix:** Fixed active object targeting in `SnapRight`, `SnapLeft`, and `SnapHead`.
* **Registration:** Fixed missing `ProxRig` unregistration and cleaned legacy code.

---

##  Installation
1. Download the latest `EpicFigRig-Blender5.zip` from the **[Releases](../../releases)** tab.
2. In Blender, go to `Edit > Preferences > Add-ons`.
3. Click the menu arrow in the top right > **Install from Disk...** and choose the downloaded zip.
4. Enable **The EpicFigRig (Blender 5.0 Fix by catdev6x)**.
5. Find the panel in the 3D Viewport sidebar (`N`-panel) under the **EpicFigRig** tab.

---

## Original JabLab Changelog (Version 1.3 - Blender 4.2)
* Fixed prop bones scaling issues
* Fixed Pivot Switch buttons
* Blender 4.2 API changes
* **More Rigging Options: Additional Objects** — will rig selected objects to the closest relevant bone
* **Updated UI:** Condensed Arm and Leg Menus; moved Smears menu to Advanced Tab
* Added Clay Meshes in between the arms with togglable visibility
* Normalize Minifigure (Early Access)
* Auto Arm Rotation (Early Access)

---

## Credits & License
* **Original Creators:** JabLab, IX Productions, Citrine's Animations, Jambo, Owenator Productions, and Golden Ninja Ben.
* **Original Repository:** [BlenderBricks/EpicFigRig](https://github.com/BlenderBricks/EpicFigRig)
* **Official Video Tutorial:** [Watch on YouTube](https://www.youtube.com/watch?v=mZM0jk-jfP0)
* **User Manual:** [Google Docs Manual](https://docs.google.com/document/d/1DUYLJnJKtjcgSzyi8djITjD8QRpN_i40ziz6wifAG0Q/edit?usp=sharing)
* **Blender 5.0 Maintenance:** @catdev6x
* Licensed under the [GNU General Public License v3.0](LICENSE).