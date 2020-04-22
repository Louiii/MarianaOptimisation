using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class GibbsMovement : MonoBehaviour
{
    public GameObject xSlice;
    public GameObject zSlice;
    private bool Up = true;

    private Vector3 center = new Vector3(465, 75, 372);
    public float speed = 4.0f;
    private float x = 415.0f;
    private float z = 372.0f;
    private float theta = 0;
    public float rad = 50.0f;
    // Start is called before the first frame update
    string m_Path;
    private int t = 0;
    public Vector3[] positions;

    void Start()
    {
        //Get the path of the Game data folder
        m_Path = Application.dataPath;

        //Output the Game data path to the console
        Debug.Log("dataPath : " + m_Path);
        positions = LoadText(m_Path + "/Paths/Gibbs.txt");
        Debug.Log(positions.Length);

        transform.transform.position = positions[0];
        Invoke("Slice", 2.0f);
    }

    public void Slice()
    {
        if (Up)
        {
            xSlice.transform.position = new Vector3(positions[t].x, 100, 500);
            xSlice.SetActive(true);
            Up = false;
        }
        else
        {
            zSlice.transform.position = new Vector3(500, 100, positions[t].z);
            zSlice.SetActive(true);
            Up = true;
        }
        Invoke("Move", 1.5f);
    }

    public void DeActivate()
    {
        xSlice.SetActive(false);
        zSlice.SetActive(false);
    }

    public void Move()
    {
        if (Up == false)
        {
            Invoke("DeActivate", 0.1f);
        }

        t += 1;
        transform.transform.position = positions[t];
        if (t < positions.Length - 1)
        {
            Invoke("Slice", 1.5f);
        }
    }

    // Update is called once per frame
    //void Update()
    //{
    //    theta += 0.01f * speed;
    //    float x = center.x + rad * Mathf.Sin(theta);
    //    float z = center.z + rad * Mathf.Cos(theta);
    //    transform.transform.position = new Vector3(x, 75, z);
    //}

    public Vector3[] LoadText(string fileName)
    {
        string[][] dataMatrix;
        string[] result = File.ReadAllLines(fileName);

        dataMatrix = new String[result.Length][];
        for (int i = 0; i < result.Length; i++)
        {

            string[] entries = result[i].Split(',');


            for (int j = 0; j < entries.Length; j++)
            {

                dataMatrix[i] = entries;
            }
        }
        Vector3[] positions = new Vector3[result.Length];
        //Array<Vector3> positions = new Array<Vector3>();
        Debug.Log("printing datamatrix");
        //Debug.Log(dataMatrix[0][0]);
        //Debug.Log(dataMatrix[1][0]);
        //Debug.Log(dataMatrix[2][0]);
        //Debug.Log(dataMatrix[3][0]);
        for (int i = 0; i < result.Length; i++)
        {
            string line = dataMatrix[i][0];
            //Debug.Log(line);
            string[] splitArray = line.Split(" "[0]);
            positions[i] = new Vector3(float.Parse(splitArray[1]) * 1000.0f,
                                       float.Parse(splitArray[2]) * 100.0f + 5.0f,
                                       float.Parse(splitArray[0]) * 1000.0f);
        }
        return positions;
    }
}

