# DBDFixSkeletons

# Discord
First things first, I have a discord server for questions, support and bugs find me here: https://discord.gg/rkkWSH2EMz

# Installation
### To install DBDFixSkeletons:
1. Go here: https://github.com/Befzz/blender3d_import_psk_psa > Right click on the 280 direct link under "Current (branch latest)" > Save Link As.
2. Go here: https://github.com/AnimNyan/DBDFixAnimations/releases > Right click on "DBDFixAnimations_v.X.X.X.zip" > Save Link As do NOT unzip it.
3. Open Blender and click Edit > Preferences > Add-Ons > Install > in the file explorer find "io_import_scene_unreal_psa_psk_280.py" and select it.
4. In the Add-Ons search, search for psk and enable the Import Unreal Skeleton Mesh Add On.
5. In the same Add-ons tab in step 3. > Install > in the file explorer find "DBDFixAnimations_v.X.X.X.zip" and select it.
6. In the Add-Ons search, search for DBDFixSkeletons and enable the Add On to complete the installation.

## What does DBDFixSkeletons do?
DBDFixSkeletons is a free Blender Plugin. It is an add on that relies on having installed Befzz's psk/psa importer. It is currently only for
fixing Killer animations imported from the game Dead By Daylight, as some animations when imported with Befzz's psk/psa importer can have
incorrect non zero keyframes attached to the Roll, IK and Jaw bones.

Thus, it is very specific and only for animations exported through UModel for the game Dead by Daylight and imported
into Blender through Befzz's psk/psa add on.

This add on will delete those keyframes from problem bones.

## How to use DBDFixSkeletons?
1. After you have clicked Import PSA to a killer skeleton using Befzz's PSK/PSA panel and the animation looks messed up, this is when you should use this script.
2. At the bottom of the PSK/PSA panel you should see a new panel named Fix DBD Animations after this add on has been installed.
3. If the jaw looks like it has problems please enable the Fix Jaw Bone box.
4. So select the skeleton with the problem animation and click Fix Dead By Daylight Killer Animation.

If you have imported multiple PSAs which all have problems. 
1. Please make sure all Actions on the Skeleton have problems, because if you "Fix" an action with no problems, it will ignore a small amount of animation data.
2. Select the skeleton with the problem actions and click Fix ALL Dead By Daylight Killer Actions to fix all actions at once.

## Disclaimer: When should this plugin not be used
Again, try not to fix make sure all Actions on the Skeleton have problems, because if you "Fix" an action with no problems, it will ignore a small amount of animation data.