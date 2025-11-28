# Pop-Off Zombies v.0.9.7

![Zombies](media/zombiesDocMain.png)

Thank you for purchasing Pop-Off Zombies, a collection of unique polygonal zombie characters with limb dismemberment, bisection, ragdoll physics, and animations.

## What's new in version v.0.9.7

- **Special Zombies:** Added two new variants: The heavy Crusher and the volatile Bloated zombie.
- **Optimization 1:** New mesh combination system reduces draw calls significantly while zombies are intact.
- **Optimization 2:** Character setup already pre-processed. (mesh processing no longer occurs on runtime)
- **Benchmark Demo:** Scene with shooting and grenades!
- **Bisection:** Zombies can now be sliced in half at the waist, creating two independent ragdolls.
- **More Animations:** Added 6 new animations to the library.


## What is included?

* *Special zombies (NEW!): Crusher and Bloated.*
* *Themed zombies: Chef, cop, construction worker, doctor, hooker, military, nun, teen boy, 
 teen girl, and waiter*
* *Generic or casual civilian types*

![special zombies](media/zombieSetp5.png)
![regular zombies](media/zombieSetp1.png)
![regular zombies](media/zombieSetp2.png)
![regular zombies](media/zombieSetp3.png)
![regular zombies](media/zombieSetp4.png)

| Asset | Count |
|-|-|
| Zombies Characters | 22 |
| Average Triangle Count | 2k |
| Animations | 16 (6 NEW!) |
| Character Materials | 1 |
| Demo materials | 3 |
| Character Textures | 2 |
| Demo Textures | 2 |
| Core Scripts (.cs) | 6 |
| Demo Scripts (.cs) | 6 |
| Demo Scenes | 2 |
| Custom Shaders | 0 |


## Demo scenes overview

### Demo_ZBench.unity

A compact shooting range where you can spawn, shoot, and blow apart dozens of zombies.

**Features:**

- Gunfire, grenades, and impact effects
- Stress test for ragdoll and dismemberment.
- Spawn and clear buttons
- FPS counter
- Day/Night toggle
- Zombie counter

Uses ZBenchCharacter and ZBenchLevelScript to demonstrate integration of movement, hit reactions, spawning, and runtime performance testing.

### Demo_Minimal.unity

Minimal scene + script to achieve bullet hit, limb detachment, ragdoll, and cut-in-half features.
([Watch video tutorial!](https://www.youtube.com/watch?v=KM876f7Sq54))

## Core Scripts and Classes

### PopRig.cs
![Zombie component](media/zombie-component.png)

The **PopRig** component is the core of the system. It manages the list of detachable limbs, the ragdoll state, and the new mesh optimization features.

**Key API Methods:**

* **`PopRig.Limbs[i].Detach()`**: Detaches a specific limb, spawning a copy with independent physics while the rest of the body continues animating.

* **`PopRig.EnableRagdoll()`**: Activates full ragdoll physics for the entire character.

* **`PopRig.CutInHalf()`**: **(New)** Splits the zombie into upper and lower halves. Both halves ragdoll independently.

* **`PopRig.SwitchToCombinedMesh()`**: **(New)** Switches the character rendering to a single combined mesh for better performance. The system automatically reverts to separated meshes when a limb is detached.

**Hit Zones**
The system now includes a static helper `HitZone PopRig.GetHitZone(Collider c)` to identify body parts easily using Raycasts or Colliders. The returned HitZone object retrives the zombie (PopRig) and limb intances like this, along with body area information (Legs, Arms, Head...)

### Limb.cs


This class represents a specific detachable body part. It handles the low-level logic of limb mesh parts, bones, and physics joints required when a part is detached.

* **`Limb.Detach()`**: Separates this specific limb.

* **`Limb.ApplyBodyImpulse(Vector3 point, Vector3 direction, float force)`**: Applies physics force to the limb. If the limb is detached, it pushes the loose part. If attached, it pushes the main body's ragdoll.

### Editor/ZombieSetupWizard.cs

Zombie Setup is accessed via the main menu **Tools/DA/Zombie Setup**. This is the artist tool to configure or modify a character for the dismembering system. It cooks the necessary data for the PopRig class. This is not needed for runtime play. All included character are already pre-configured.



## Starting Guide

From version 0.9.7, character are preprocessed and ready for play mode.

- To start, drag any of the character prefabs to the scene.
- From anywhere you do a Physics Cast, call static PopRig.GetHitZone() to retrive information linked to the given Collider: PopRig and Limbs instances, Body zone, etc.
- Use methods like Limb.Detach() to pop-off zombie parts, or play with PopRig.EnableRagdoll() and PopRig.CutInHalf().
- Code your own scripts that interact with the Zombie component to trigger limbs detachments or body ragdolls when you decide.

### [>> Watch Minimal-Demo Video Tutorial!](https://www.youtube.com/watch?v=KM876f7Sq54)

**NOTE:** There is no AI behaviour, health system, or pathfinding implemented, it is up to your gameplay mechanics and particular needs.

## Roadmap

- Add a new set of ~8 special zombies.
- More animations: Pain, stand up from ground, etc.
- Basic NPC AI examples.

## Support and Feedback

This project is evolving, anything could be changed to improve or add more features.  

Your feedback is important! If you have any comments, questions, or need assistance, please reach out at [denys.almaral@gmail.com](mailto:denys.almaral@gmail.com).

*Let's get ready to zzzombieeeee!*