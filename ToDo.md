# [to Main](./README.md)

## Unity Event Functions

## ```GetComponent<T>()```

<!-- TODO -->

* [GameObject.SetAсtive(value) vs. Component.enabled = value](./Pages/SideBySideComparison/GOSetActiveVSComponentEnabled.md)




## ```.transform``` and ```.gameObject```

## Garbage Collection (GC)

### ```StringBuilder``` vs ```+``` vs ```string.Format(args)```/```$"{}"```
bla bla, string is not a struct, bla bla ```"str1" + "str2"``` just slower and maes gc
### ```.tag == someString``` vs 
### GC of yeild return new WaitForSeconds(value);
You can look at the talk on Unity forums where it is discussed. Sometimes I observe that looks roughly like this:

```csharp
protected System.Collections.IEnumerator DoSomeCoroutine()
{
    for (;;)
    {
        yield return new UnityEngine.WaitForEndOfFrame();
    }
}
```
which is not exactly the expected way of using Coroutines.



## Tags vs Layers vs Camera Depth

## Containers from ```System.Collections.Generics```


## Serialization

## Editor Scripts
### Editor
### PropertyDrawer

## Console Messages 

```csharp
Debug.LogFormat("<color=yellow>WARNING: {0} is </color>", someParameter);
```

## ```C#``` in Unity, compiling

## IDE
### Jetbrains Rider
Don't forget to use your IDE wisely rather than having all the things from the box. Learning your IDE requires roughly as much effort as Unity Editor, but you definetely save your time if wisely set up your work one.

[Place field attribute on the same line > Never](https://rider-support.jetbrains.com/hc/en-us/community/posts/360004233720-How-do-I-allow-Unity-attributes-to-be-on-their-own-line-)

```csharp
public class WhateverMB : MonoBehaviour
{
    // to make
    [SerializeField]
    protected Dropdown dropdown;

    // instead of
    [SerializeField] protected Dropdown dropdown;
}
```

### Microsoft Visual Studio
Feel free to contribute

### Microsoft Visual Studio Code
Feel free to contribute

