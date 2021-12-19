*Test Setup*: there were 100x100 Objects spawned, each had a sphere mesh, one MeshRenderer and 1-16 ```BoxCollider```s. Actually also Sphere collider, forgot to remove it, but doesnt matter, I dont update it.

**Prefab structure**
* ROOT_GO
  * UnityUpdateComponentsEnableMB(Clone)
    * Sphere (**1** ```MeshRenderer```, **1-16** ```BoxCollider```**(s)**, ```MeshFilter``` and ```SphereCollider```)
  * UnityUpdateComponentsEnableMB(Clone)
    * Sphere (**1** ```MeshRenderer```, **1-16** ```BoxCollider```**(s)**, ```MeshFilter``` and ```SphereCollider```)
  * etc, 100x100 of UnityUpdateComponentsEnableMB.

Below are the code samples I used for testing:

```csharp
// UnityUpdateGOSetActiveEachMB.cs
protected void Update()
{
    // T1: it is fair to make a variable same is for T2 and T3
    // sphere is SphereRenderer.gameObject
    var isEnabled = Time.frameCount % 2 == 0;
    sphere.SetActive(isEnabled);
}
// UnityUpdateComponentsEnableMB.cs
protected void Update()
{
    // T2 and T3 were commented out and were tested separately
    var isEnabled = Time.frameCount % 2 == 0;

    // T2: SphereRenderer is MeshRenderer
    SphereRenderer.enabled = isEnabled;
    
    // T3: SphereBoxColliders is List<BoxCollider>
    for (int i = 0; i < numberOfComponents; ++i)
    {
        SphereBoxColliders[i].enabled = isEnabled;
    }
}
```

In update I 1. Enable/disable whole game object, 2. Mesh renderer, 3. Forloop every box collider

Test: 1, number of ```BoxCollider```s is 1
|№| Test                                                   | FPS       |
|-| -                                                      | ---------:|
|1: **1** ```BoxCollider```  |                             |           |
|                   | ```GameObject.SetActive()```         | 12.8-14   |
|                   | 1 ```MeshRenderer```                 | 33-35     |
|                   | 1 ```BoxCollider``` for-loop         | 19.5-20.5 |
|2: **2** ```BoxCollider```s |                             |           |
|                   | ```GameObject.SetActive()```         | 10.5-11   |
|                   | 1 ```MeshRenderer```                 | 35-37     |  
|                   | 2 ```BoxCollider``` for-loop         | 12.4-12.8 |
|3: **4** ```BoxCollider```s |                             |           |
|                   | ```GameObject.SetActive()```         | 7.6-8.8   |
|                   | 1 ```MeshRenderer```                 | 32-35     |
|                   | 4 ```BoxCollider``` for-loop         | 7.9-8.6   |
|4: **8** ```BoxCollider```s |                             |           |
|                   | ```GameObject.SetActive()```         | 5.2-5.6   |
|                   | 1 ```MeshRenderer```                 | 32-35     |
|                   | 8 ```BoxCollider``` for-loop         | 4.8-5     |
|5: **16** ```BoxCollider```s|                             |           |
|                   | ```GameObject.SetActive()```         | 3.4-3.5   |
|                   | 1 ```MeshRenderer```                 | 31-32     |
|                   | 16 ```BoxCollider``` for-loop        | 1.9-3.1   |

*Results Interpretation*: when there are just a few components attached to a GameObject, it is more costly to disable the whole GameObject. Disabling particular conponents would be better. However, when there are more Components, *roughly 6+* per GO, it seems that iterating them in for-loop seems to be less effective than disabling using GameObject.SetActive(false); because it is done better by Unity on the engine level.

The second test evaluates a scenario when Enabled/Disabled GameObject has children in the hierarchy versus Enabling/Disabling particular components. This time it is ```MeshRenderer```. Below is the structure of prefab:

**Prefab structure**
* ROOT_GO
  * UnityUpdateGOHasChildren(Clone)
    * Sphere (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```)
      * SphereInstantiated(Clone) (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```);
      * SphereInstantiated(Clone) (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```);
      * SphereInstantiated(Clone) (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```);
      * etc, Total 1-16 SphereInstantiated based on Test №, see below
  * UnityUpdateGOHasChildren(Clone)
    * Sphere (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```)
      * SphereInstantiated(Clone) (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```);
      * SphereInstantiated(Clone) (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```);
      * SphereInstantiated(Clone) (**1** ```MeshRenderer```, ```MeshFilter``` and ```SphereCollider```);
      * etc, Total 1-16 SphereInstantiated based on Test №, see below
  * etc, 100x100 of UnityUpdateGOHasChildren.

|№| Test                                                  | FPS       |
|-| -                                                     | ---------:|
|1: **1** ```BoxCollider```  |                            |           |
|                   | Parent ```GameObject.SetActive()``` | 8-10      |
|                   | 1 ```MeshRenderer``` for-loop       | 21.7-23.3 |
|2: **2** ```BoxCollider```s |                            |           |
|                   | Parent ```GameObject.SetActive()``` | 5.9-7.7   |  
|                   | 2 ```MeshRenderer``` for-loop       | 13.6-16.5 |
|3: **4** ```BoxCollider```s |                            |           |
|                   | Parent ```GameObject.SetActive()``` | 4.2-4.3   |
|                   | 4 ```MeshRenderer``` for-loop       | 8.9-9.1   |
|4: **8** ```BoxCollider```s |                            |           |
|                   | Parent ```GameObject.SetActive()``` | 2.6-2.7   |
|                   | 8 ```MeshRenderer``` for-loop       | 4.8-5.2   |
|5: **16** ```BoxCollider```s|                            |           |
|                   | Parent ```GameObject.SetActive()``` | ~0.2-1*   |
|                   | 16 ```MeshRenderer``` for-loop      | 2.6-2.7   |

\~0.2-1* the game just didn't manage at that point and I can conclude that having abusing all the potential of Hierarchies is dangerous.

