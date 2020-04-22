using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CamMovement : MonoBehaviour
{
    Vector3 target = new Vector3(500.0f, 316.0f, 500.0f);
    Vector3 viewtarget = new Vector3(500.0f, -200.0f, 500.0f);
    float theta = -1.0f;
    float radius = 650.0f;

    //void Start()
    //{
    //    this.transform.position = new Vector3(100.0f, 316.0f, 500.0f);
    //    this.transform.rotation = new Quaternion(67.0f, 90.0f, 0.0f, 0.0f);
    //}

    void LateUpdate()
    {
        theta += 0.0005f;
        transform.position = new Vector3(target.x - radius * Mathf.Cos(theta), target.y, target.z + radius * Mathf.Sin(theta));
        transform.LookAt(viewtarget);
    }
}
