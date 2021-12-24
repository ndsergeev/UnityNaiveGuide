# [to Main](../../README.md)

# Script Templates

It is a very handy to adjust your script templates to make files that already have all the required setup. Simple use case can be legal notice that you can also do with code snippets..., but isn't having a script template easier? When the size of your project turns really big, it becomes quite handy. In addition to legal notice you can customize your template to make preset for DOTS or any other custom systems, e.g. [NightCache C# Script Template](https://github.com/ndsergeev/NightCache/blob/main/ScriptTemplates/81-C%23%20Script-NewBehaviourScript.cs.txt).

## Add Custom templates

There are a few ways to make your script templates. The most convinient, easiest is to create a folder called ```ScriptTemplates``` under your ```Assets```. Inside you should create, for instance, ```81-C# Script-NewBehaviourScript.cs.txt```. This template should override your default 'C# Script' in the Right-Click menu in 'Project' Unity Editor window. '81' is the number that is used for ordering in that menu, same as order that you put in ```CreateAssetMenu()``` when make ScriptableObject. If you put 82, 83 or any other, with the same ending, your script will appear above/below as a *duplicate*, if the number is the same, but you, lets say, put "```81-```**B**```# Script```", then it should appear above. This way you don't override the script, that is why you should have the part "```81-C# Script```" identical. However, you are free to change ```NewBehaviourScript```, that is how the default name of the script will look like.

*Note*: these script templates do not override script creation if you create with "Add Component" -> "New Script" via Inspector Window. Unfortunately, if you need this, it is available in the Unity app directory, see below paths corresponding to different platforms.

The number of scripts that you/your studio uses can be different. If it is extensive, you can group your options with "__", **double** underscore. For example, you can have your scripts under **Fancy Studios Templates** like: 

```81-Fancy Studios Templates__C# Class-NewClass.cs.txt``` \
```81-Fancy Studios Templates__C# Interface-NewInterface.cs.txt``` \
```81-Fancy Studios Templates__C# Scriptable Object-NewScriptableObjectScript.cs.txt```

A few words about how your template *can* look. I normally avoid ```target``` and use only ```serializedObject```, but it can be a good illustration. Also, for Editor script it is fine if file name and class names are different. So when you create your Editor script you can name it the same as ```MonoBehaviour``` class, they are in different assemblies.

```cs
//////////////////////////////
///  Not production-ready  ///
//////////////////////////////

using UnityEditor;

namespace NAMESPACE
{
    [CustomEditor(typeof(#SCRIPTNAME#))]
    public class #SCRIPTNAME#Editor : Editor
    {
        private void OnEnable()
        {
            #NOTRIM#
        }

        /// <summary>
        /// <see cref="#SCRIPTNAME#"/>
        /// </summary>
        public override void OnInspectorGUI()
        {
            var #SCRIPTNAME_LOWER# = (#SCRIPTNAME#)target;
            
            EditorGUI.BeginDisabledGroup(true);
            EditorGUILayout.PropertyField(serializedObject.FindProperty("m_Script"));
            EditorGUI.EndDisabledGroup();
            
            // var serializedPropertyMyInt = serializedObject.FindProperty("");
            //serializedObject.ApplyModifiedProperties();
        }
    }
}
```

* **#SCRIPTNAME#** -- Replaces it with the filename on script creation.
* **#SCRIPTNAME_LOWER#** -- Similar as the one above, but changes the first uppercase letter to lowercase. Before if you name your file with lowercase as first letter, it was removing all the lowercase letters until it reaches uppercase. Now Unity adds 'my' prefix. So if filename is ```scriptMB``` then it swaps ```#SCRIPTNAME_LOWER#``` to ```myScriptMB```.
* **#NOTRIM#** -- Lets parser know not to clean this empty line, e.g. empty function. However, it might not have any effect. It can preserve many tabulations which, I recon, you don't need.

## Original Templates

Locations of original files:
* MacOS
  * Unity: <!-- TODO -->
  * UnityHub: ```*/UnityInstalls/*/Unity.app/Contents/Resources/ScriptTemplates```
* Windows
  * Unity: <!-- TODO -->
  * UnityHub: <!-- TODO -->
* Linux
  * Unity: <!-- TODO -->
  * UnityHub: <!-- TODO -->

## Handle Manually

<!-- TODO: write about the option when you do the same via Editor Scripts -->
