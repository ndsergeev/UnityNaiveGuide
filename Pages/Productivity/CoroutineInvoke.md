# [to Main](../../README.md)

## Coroutines vs Invoke vs Async/Await

### Coroutine

### Invoke
The official page of [MonoBehaviour.Invoke](https://docs.unity3d.com/ScriptReference/MonoBehaviour.Invoke.html) sasy "For better performance and maintability, use [Coroutines](https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity3.html) instead." Additionally, it is inconvinient to use ```Invoke``` as, when you refactor, you might not change the string function parameter in ```Invoke``` via your IDE. Note, it is the only issue for C# versions earlier than 6. From v6 there is an expression ```nameof()``` which will replace function name with string.

```csharp
class WaiterMB : MonoBehaviour
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
class WaiterMB : MonoBehaviour
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

### Opinion

There is a ```StopAllCoroutines()``` that I try to avoid and do ```StopCoroutine(SomeCoroutine)``` instead as there is a chance to produce an unexpected behaviour. For example, you can have a class hierarchy where you have implemented your coroutine. You kept only one so felt safe to put ```StopAllCoroutines()```. Later someone inherited from that class and made another Coroutine. So if that ```StopAllCoroutines()``` is called when the second or both are executing, then it cause unexpected behaviour. The example can also work if there is a Coroutine in a parent class and ```StopAllCoroutines()``` in child. So don't try remembering all the fields of your classes, it is just a good habbit to stop individual Coroutines when needed via ```StopCoroutine(SomeCoroutine)```.

#### Async/Await

<!-- TODO -->

You can also [Looking into Unity's async/await](https://gametorrahod.com/unity-and-async-await/)
