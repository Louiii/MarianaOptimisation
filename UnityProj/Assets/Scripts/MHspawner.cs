using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class MHspawner : MonoBehaviour
{
    public GameObject mhBall;
    private GameObject[] mhBalls;
    void Start()
    {
        string m_Path = Application.dataPath;
        for (int i = 0; i < 10; i++)
        {
            Instantiate(mhBall, new Vector3(0, 0, 0), Quaternion.identity);
        }
        mhBalls = GameObject.FindGameObjectsWithTag("MH");

        for (int i = 0; i < mhBalls.Length; i++)
        {
            mhBalls[i].GetComponent<Movement>().positions = LoadText(m_Path + "/Paths/MHs/MH" + i.ToString() + ".txt");
            mhBalls[i].GetComponent<Movement>().Hop();
        }
    }

    public void Clear()
    {
        for (int i = 0; i < mhBalls.Length; i++)
        {
            Destroy(mhBalls[i]);
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