using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class Movement : MonoBehaviour
{
    [HideInInspector] // Hides var below
    public Vector3[] positions;
    private int t = 0;
    // Start is called before the first frame update
    void Start()
    {
    }

    public void Hop()
    {
        transform.transform.position = positions[t];
        t += 1;
        if (t < positions.Length - 1)
        {
            Invoke("Hop", 0.04f);
        }
    }

}

