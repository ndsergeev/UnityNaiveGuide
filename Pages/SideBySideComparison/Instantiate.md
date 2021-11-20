# [to Main](../../README.md)

## ```Instantiate<T>()```

Well, everyone knows that it is a bad idea to abuse that function. Just make sure you don't do as well this. *Yes, I saw that many times, so don't make that expensive function take even more time for no reason, all of those can be other parameters of* ```Instantiate<T>()```.
```csharp
protected void Spawner()
{
    for (int i = 0; i < YOUR_LIST.Count; ++i)
    {
        var component = Instantiate<YOUR_TYPE>(prefab); 
        component.transform.parent = transform;
        component.transform.position = Vector3.zero;
        // something else, mb rotation. Again this is how NOT to do
    }
}
```