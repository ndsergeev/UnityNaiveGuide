# UnityNaiveGuide

## Preface

Probably the main question that you might have once reaching this page and seing lots of text which varies in quality: "Is it one more Unity Guide?"\
\- Yes. There are so many damn good resources on the web that sometimes it is difficult to find them all until you search for something very specific. I will put here all of those as well as some other tests I do in spare time (if I am even capable to compete with those bright minds who help improving my everydays code). I hope that set of practises here can be a good starting poing for someone. The text will have many alterations as long as I or other contributors learn new things about Unity.

I'd like to mention that not all the tests and recommendations can fit your project. **I belive that every line is written here makes you more suspicios, resulting in validating the information you are after on here** and then contributing to this guide with your clarifications. Highly appreciate this approach, so lets learn together!

It is important to mention that the tests that are provided in this guide should be considered quite sceptically. I believe that if you really want to compare two or more operations on which performance is better, then it is fair to compare on the level of instructions. However, I don't have the access to Unity's source code as well as I am not a specialist to go that deep to disassemble code. That is why all I can do is running some tests, which, sometimes, can be far from what you might face in production.

*PS, if you want to tell me at some point of reading that some of my examples are far-fetched and/or stupid, that they don't pass peer review in big teams – I am very proud for your team and still sure that not all the teams are like yours!*

## TOC

## Productivity

* [Script Templates](./Pages/Productivity/ScriptTemplates.md)

* [Project Templates](./Pages/Productivity/ProjectTemplates.md)

## Unity Event Functions

## ```GetComponent<T>()```

<!-- TODO -->

## ```Instantiate<T>()```

Well, everyone knows that it is a bad idea to abuse that function. Just make sure you don't do as well this. *Yes, I saw that many times, so don't make that expensive function take even more time for no reason, all of those can be other parameters of* ```Instantiate<T>()```.
```csharp
private void Whatever()
{
    for (int i = 0; i < YOUR_LIST.Count; ++i)
    {
        var component = Instantiate<YOUR_TYPE>(prefab); 
        component.transform.parent = transform;
        component.transform.position = Vector3.zero;
        // something else, mb rotation
    }
}
```

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


### Coroutines vs Invoke vs Async/Await

#### Coroutine

#### Invoke
In addition to what is mentioned on the official page of [MonoBehaviour.Invoke](https://docs.unity3d.com/ScriptReference/MonoBehaviour.Invoke.html): "For better performance and maintability, use [Coroutines](https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity3.html) instead." it is inconvinient to use ```Invoke``` as, when you refactor, you might not change the string function parameter in ```Invoke``` via your IDE. Note, it is the only issue for C# versions earlier than 6. From v6 there is an expression ```nameof()``` which will replace function name with string.

```csharp
class Whatever : MonoBehaviour
{
    protected void DoSomeVoid()
    {
        Invoke("DoInvoke", 0.5f);
        Invoke(nameof(DoInvoke), 0.5f); // from C# 6
    }

    protected void DoInvoke()
    {
        // do stuff
    }
}
```

It is not difficult to rewrite your ```Invoke``` with coroutines:

```csharp
class WhateverMB : MonoBehaviour
{
    protected WaitForSeconds WaitForSomeSeconds = new WaitForSeconds(0.5f);
    protected Coroutine SomeCoroutine = null;

    protected void DoSomeDelayedVoid()
    {
        if (SomeCoroutine != null)
        {
            StopCoroutine(SomeCoroutine);
        }
        SomeCoroutine = StartCoroutine(DoSomeCoroutine());
    }
    
    protected System.Collections.IEnumerator DoSomeCoroutine()
    {
        yield return WaitForSomeSeconds;
        // do stuff
    }
}
```
There is a ```StopAllCoroutines()``` that I try to avoid and do ```StopCoroutine(SomeCoroutine)``` instead as there is a chance to produce an unexpected behaviour. For example, you can have a class hierarchy where you have implemented your coroutine. You kept only one so felt safe to put ```StopAllCoroutines()```. Later someone inherited from that class and made another Coroutine. So if that ```StopAllCoroutines()``` is called when the second or both are executing, then it cause unexpected behaviour. The example can also work if there is a Coroutine in a parent class and ```StopAllCoroutines()``` in child. So don't try remembering all the fields of your classes, it is just a good habbit to stop individual Coroutines when needed via ```StopCoroutine(SomeCoroutine)```.

#### Async/Await
You can also [Looking into Unity's async/await](https://gametorrahod.com/unity-and-async-await/)


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

