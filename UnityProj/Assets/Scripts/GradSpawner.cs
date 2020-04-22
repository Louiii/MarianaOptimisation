using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class GradSpawner : MonoBehaviour
{
    public GameObject gradBall;
    private GameObject[] gradBalls;
    void Start()
    {
        string m_Path = Application.dataPath;
        for (int i = 0; i < 49; i++)
        {
            Instantiate(gradBall, new Vector3(0, 0, 0), Quaternion.identity);
        }
        gradBalls = GameObject.FindGameObjectsWithTag("Grad");

        for (int i = 0; i < gradBalls.Length; i++)
        {
            gradBalls[i].GetComponent<GradMovement>().positions = LoadText(m_Path + "/Paths/GradDescs/G" + i.ToString() + ".txt");
            gradBalls[i].GetComponent<GradMovement>().Hop();
        }
    }

    public void Clear()
    {
        for (int i = 0; i < gradBalls.Length; i++)
        {
            Destroy(gradBalls[i]);
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
