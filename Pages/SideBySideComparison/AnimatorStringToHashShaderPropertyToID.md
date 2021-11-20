# [to Main](../../README.md)

## ```Shader.PropertyToID("")``` and ```Animator.StringToHash("")```

The offcial pages for [Animator.StringToHash](https://docs.unity3d.com/ScriptReference/Animator.StringToHash.html) and [Shader.PropertyToID](https://docs.unity3d.com/ScriptReference/Shader.PropertyToID.html), where it clearly say "IDs are used for optimized setters and getters..." and "using property identifiers is more efficient than passing strings..." respectively. So you can consider avoiding strings as the parameter when you call any of these.

<!-- TODO: make prots instead of that row data in tables -->

### Probably a Better Approach

IDEs, e.g. as Rider, automatically recognise similar cases in your project and suggest to hash ```string```s into ```int```s. However, over time you might encounter duplicates of the same parameters and it is probably better to have a special place for all of them. The example below also allows you to control all the names in one file. There is also an option to make a configue file or ScriptableObject file for that, but the simplest example is below:

```csharp
namespace Test.Properties
{
    using UnityEngine;

    public static class AnimatorProperties
    {
        public static readonly int RotateYAnimationClip = Animator.StringToHash("RotateY");
        public static readonly int RotateZAnimationClip = Animator.StringToHash("RotateZ");
    }
    public static class ShaderProperties
    {
        public static readonly int ColorShaderProperty = Shader.PropertyToID("_Color");
        public static readonly int TintShaderProperty = Shader.PropertyToID("_Tint");
    }

    // OR
    [CreateAssetMenu(fileName = "Properties", menuName = "ScriptableObjects/Properties")]
    public class PropertiesSO : ScriptableObject
    {
        public readonly int RotateYAnimationClip = Animator.StringToHash("RotateY");
        public readonly int RotateZAnimationClip = Animator.StringToHash("RotateZ");

        public readonly int ColorShaderProperty = Shader.PropertyToID("_Color");
        public readonly int TintShaderProperty = Shader.PropertyToID("_Tint");
    }
}
```

### Example for Animators: 

```csharp
namespace Tests.HashingStrings.Animators
{
    using UnityEngine;
    
    using HashedProperties;

    public class AnimationChangerMB : MonoBehaviour
    {
        [SerializeField]
        protected GameObject sphere1;
        [SerializeField]
        protected GameObject sphere2;
        
        protected bool Swapper = false;
        protected Animator Sphere1Animator;
        protected Animator Sphere2Animator;
        
        protected void Awake()
        {
            Sphere1Animator = sphere1.GetComponent<Animator>();
            Sphere2Animator = sphere2.GetComponent<Animator>();
        }

        protected void Update()
        {
            if (!Input.GetKeyDown(KeyCode.Tab))
                return;
                
            if (Swapper)
            { 
                Sphere1Animator.Play(AnimatorProperties.RotateZAnimationClip); 
                Sphere2Animator.Play(AnimatorProperties.RotateYAnimationClip);
            }
            else
            {
                Sphere1Animator.Play(AnimatorProperties.RotateYAnimationClip);
                Sphere2Animator.Play(AnimatorProperties.RotateZAnimationClip); 
            }
            Swapper = !Swapper;
        }
    }
}
```

#### Performance

* Test #1 – Execute with string e.g. ```Sphere1Animator.Play("RotateZ");```
* Test #2 – Execute with locally cached int value;
* Test #3 – Execute with static int from static class;
* Test #4 – Same as above, but value was cached before loop;
* Test #5 – Execute with int from ScriptableObject class;
* Test #6 – Same as above, but value was cached before loop.

#### Editor

|Times       | Test #1    | Test #2    | Test #3    | Test #4    | Test #5    | Test #6    |
|-           | -:         | -:         | -:         | -:         | -:         | -:         |
| 1          | 0.00014849 | 0.00007170 | 0.00000700 | 0.00001120 | 0.00000738 | 0.00001053 |
| 1          | 0.00000515 | 0.00000505 | 0.00000321 | 0.00000467 | 0.00000475 | 0.00000306 |
| 10         | 0.00000666 | 0.00000404 | 0.00000669 | 0.00000592 | 0.00000386 | 0.00000384 |
| 100        | 0.00002740 | 0.00002500 | 0.00001750 | 0.00002276 | 0.00001755 | 0.00001788 |
| 1000       | 0.00033476 | 0.00015649 | 0.00020201 | 0.00015632 | 0.00015598 | 0.00023105 |
| 10000      | 0.00240798 | 0.00155762 | 0.00133051 | 0.00140078 | 0.00166718 | 0.00153883 |
| 100000     | 0.01805707 | 0.01114511 | 0.01113095 | 0.01122464 | 0.01120038 | 0.01113555 |
| 1000000    | 0.14642538 | 0.09188678 | 0.09118677 | 0.09149084 | 0.09296595 | 0.09170776 |
| 10000000   | 1.38090207 | 0.90337447 | 0.90877167 | 0.91157750 | 0.91057538 | 0.94460000 |

#### IL2CPP MacOS Intel 64-bit

|Times       | Test #1    | Test #2    | Test #3    | Test #4    | Test #5    | Test #6    |
|-           | -:         | -:         | -:         | -:         | -:         | -:         |
| 1          | 0.00000887 | 0.00000081 | 0.00000183 | 0.00000223 | 0.00000204 | 0.00000220 |
| 1          | 0.00000457 | 0.00000221 | 0.00000232 | 0.00000203 | 0.00000191 | 0.00000214 |
| 10         | 0.00001018 | 0.00000407 | 0.00000394 | 0.00000421 | 0.00000356 | 0.00000364 |
| 100        | 0.00002641 | 0.00001685 | 0.00001701 | 0.00001661 | 0.00001667 | 0.00001705 |
| 1000       | 0.00024906 | 0.00014647 | 0.00016511 | 0.00016372 | 0.00016302 | 0.00014549 |
| 10000      | 0.00235644 | 0.00149591 | 0.00156760 | 0.00150800 | 0.00151446 | 0.00147985 |
| 100000     | 0.01664717 | 0.01035973 | 0.00960241 | 0.00968604 | 0.00914258 | 0.01052656 |
| 1000000    | 0.10926833 | 0.06973652 | 0.07076260 | 0.07580751 | 0.07004646 | 0.07040648 |
| 10000000   | 1.00485862 | 0.63289100 | 0.63487495 | 0.63104334 | 0.63236006 | 0.63263087 |


### Example for Shaders:
If you make different shaders with the same parameter name, e.g. ```"_Color"```, there should be no problems to **re**use it for different shaders. Unity recalculates value, so there should be no collision. You can try it yourself: just make two spheres with different materials & shaders. Have a property of the same name and type in both shaders, the one you'll access with ```.SetColor()```, ```.SetFloat()``` etc.

```csharp
namespace Tests.HashingStrings.Shaders
{
    using UnityEngine;
    
    using HashedProperties;

    public class ColorChangerMB : MonoBehaviour
    {
        [SerializeField]
        protected GameObject sphere1;
        [SerializeField]
        protected GameObject sphere2;

        protected Material Sphere1Material;
        protected Material Sphere2Material;
        
        protected void Awake()
        {
            Sphere1Material = sphere1.GetComponent<Renderer>().sharedMaterial;
            Sphere2Material = sphere2.GetComponent<Renderer>().sharedMaterial;
        }

        protected void Update()
        {
            if (!Input.GetKeyDown(KeyCode.Space))
                return;
            var color1R = Random.Range(0f, 1f);
            var color1G = Random.Range(0f, 1f);
            var color1B = Random.Range(0f, 1f);
            
            Sphere1Material.SetColor(ShaderProperties.ColorShaderProperty,
                new Color(color1R, color1G, color1B, 1f));
            
            var color2R = Random.Range(0f, 1f);
            var color2G = Random.Range(0f, 1f);
            var color2B = Random.Range(0f, 1f);
            
            Sphere2Material.SetColor(ShaderProperties.ColorShaderProperty,
                new Color(color1R, color1G, color1B, 1f));
            // Sphere2Material.SetColor(ShaderProperties.ColorShaderProperty,
            //     new Color(color2R, color2G, color2B, 1f));
        }
    }
}
```

Just make two spheres, two materials and two shaders for them. Put the code below in your shaders for ```Sphere_1``` and ```Sphere_2``` respectively.

```glsl
Shader "Unlit/Sphere_1" // Shader "Unlit/Sphere_2"
{  
    Properties { _Color ("Main Color", Color) = (1,1,1,1) }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100
        
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            struct appdata
            {
                float4 vertex : POSITION;
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
            };

            float4 _Color;

            v2f vert (appdata v) {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return _Color;      // Shader "Unlit/Sphere_1"
                return 1 - _Color;  // Shader "Unlit/Sphere_2"
            }
            ENDCG
        }
    }
}
```

#### Performance

* Test #1 – Execute with string e.g. ```Sphere1Material.SetColor("_Color", SomeColour);```
* Test #2 – Execute with locally cached int value;
* Test #3 – Execute with static int from static class;
* Test #4 – Same as above, but value was cached before loop;
* Test #5 – Execute with int from ScriptableObject class;
* Test #6 – Same as above, but value was cached before loop.

#### Editor

|Times     | Test #1    | Test #2    | Test #3    | Test #4    | Test #5    | Test #6    |
|-         | -:         | -:         | -:         | -:         | -:         | -:         |
| 1        | 0.00000831 | 0.00007536 | 0.00002213 | 0.00000792 | 0.00000742 | 0.00000848 |
| 1 again  | 0.00000742 | 0.00000383 | 0.00000318 | 0.00000312 | 0.00000321 | 0.00000183 |
| 10       | 0.00000503 | 0.00000458 | 0.00000430 | 0.00000523 | 0.00000454 | 0.00000515 |
| 100      | 0.00002602 | 0.00001307 | 0.00001299 | 0.00001517 | 0.00001715 | 0.00001714 |
| 1000     | 0.00026692 | 0.00012060 | 0.00011721 | 0.00015282 | 0.00015758 | 0.00011767 |
| 10000    | 0.00206858 | 0.00093458 | 0.00114345 | 0.00094270 | 0.00093802 | 0.00093176 |
| 100000   | 0.01528322 | 0.00805394 | 0.00815373 | 0.00802989 | 0.00792480 | 0.00802744 |
| 1000000  | 0.12462365 | 0.06748622 | 0.06878386 | 0.07070566 | 0.06860883 | 0.06701352 |
| 10000000 | 1.18080147 | 0.65498759 | 0.65808497 | 0.65136666 | 0.65934728 | 0.65718837 |

#### IL2CPP MacOS Intel 64-bit

|Times     | Test #1    | Test #2    | Test #3    | Test #4    | Test #5    | Test #6    |
|-         | -:         | -:         | -:         | -:         | -:         | -:         |
| 1        | 0.00001183 | 0.00000180 | 0.00000127 | 0.00000151 | 0.00000284 | 0.00000312 |
| 1 again  | 0.00001055 | 0.00000188 | 0.00000180 | 0.00000172 | 0.00000167 | 0.00000217 |
| 10       | 0.00000690 | 0.00000307 | 0.00000323 | 0.00000564 | 0.00000318 | 0.00000355 |
| 100      | 0.00002648 | 0.00001332 | 0.00006365 | 0.00001357 | 0.00001278 | 0.00001380 |
| 1000     | 0.00023381 | 0.00011365 | 0.00011388 | 0.00019378 | 0.00013290 | 0.00011368 |
| 10000    | 0.00233917 | 0.00120554 | 0.00119545 | 0.00116674 | 0.00118861 | 0.00117835 |
| 100000   | 0.01656655 | 0.00874680 | 0.00864122 | 0.00908912 | 0.00848267 | 0.00857170 |
| 1000000  | 0.11665278 | 0.05940517 | 0.05452891 | 0.05607068 | 0.05616178 | 0.05674499 |
| 10000000 | 1.00733784 | 0.49475148 | 0.50794711 | 0.49516667 | 0.49861623 | 0.49419712 |


### Opinion

it is hard to imagine that you have a real reason to update your shader property in the same frame for more than 10-100 materials. If you do so, probably you have to consider how to reuse your materials. If you can reuse your materials Unity could properly use batching. It is clearly 1.5-2x boost if avoiding ```string```s as a parameter. 

Practically you can see that it is fine to have a separate class to keep your properties. From management perspective it is just easier to change things in one place. Static class or a SO is a preference thing, it only can be quite annoying to assign refereneces if you don't make a singleton or don't automate assigning for your SO. Making a local variable for this case is not useful much.

<!-- TODO: finish, as I remember SO will exist as long as it has references to it, so seems like it is not THAT different from static class, at least from the use perspective and mem-management perspective. -->
