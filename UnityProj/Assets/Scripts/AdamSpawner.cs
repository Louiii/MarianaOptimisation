using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class AdamSpawner : MonoBehaviour
{
    public GameObject adamBall;
    private GameObject[] adamBalls;

    void Start()
    {
        string m_Path = Application.dataPath;
        for (int i = 0; i < 49; i++)
        {
            Instantiate(adamBall, new Vector3(0, 0, 0), Quaternion.identity);
        }
        adamBalls = GameObject.FindGameObjectsWithTag("Adam");

        for (int i = 0; i < adamBalls.Length; i++)
        {
            adamBalls[i].GetComponent<AdamMovement>().positions = LoadText(m_Path + "/Paths/Adam/A" + i.ToString() + ".txt");
            adamBalls[i].GetComponent<AdamMovement>().Hop();
        }
    }

    public void Clear()
    {
        for (int i = 0; i < adamBalls.Length; i++)
        {
            Destroy(adamBalls[i]);
        }
    }

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
        Vector3[] pos = new Vector3[result.Length];
        for (int i = 0; i < result.Length; i++)
        {
            string line = dataMatrix[i][0];
            string[] splitArray = line.Split(" "[0]);
            pos[i] = new Vector3(float.Parse(splitArray[1]) * 1000.0f,
                                       float.Parse(splitArray[2]) * 100.0f + 5.0f,
                                       float.Parse(splitArray[0]) * 1000.0f);
        }
        return pos;
    }
}
