using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class BeeHive : MonoBehaviour
{
    public GameObject bee;
    private GameObject[] bees;
    void Start()
    {
        string m_Path = Application.dataPath;
        //make lots of bees
        for (int i = 0; i < 20; i++)
        {
            Instantiate(bee, new Vector3(0, 0, 0), Quaternion.identity);
            //GameObject beeobj = 
            //bee.GetComponent<Beehaviour>().positions = LoadText(m_Path + "/Paths/Bees/Bee"+i.ToString() + ".txt");
            //Debug.Log(bee.GetComponent<Beehaviour>().positions);
            //bee.GetComponent<Beehaviour>().Hop();
        }
        bees = GameObject.FindGameObjectsWithTag("Bee");

        for (int i = 0; i < bees.Length; i++)
        {
            bees[i].GetComponent<Beehaviour>().positions = LoadText(m_Path + "/Paths/Bees/Bee" + i.ToString() + ".txt");
            bees[i].GetComponent<Beehaviour>().Hop();
        }
    }

    public void Clear()
    {
        for (int i = 0; i < bees.Length; i++)
        {
            Destroy(bees[i]);
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
        //Array<Vector3> positions = new Array<Vector3>();
        //Debug.Log("printing datamatrix");
        //Debug.Log(dataMatrix[0][0]);
        //Debug.Log(dataMatrix[1][0]);
        //Debug.Log(dataMatrix[2][0]);
        //Debug.Log(dataMatrix[3][0]);
        for (int i = 0; i < result.Length; i++)
        {
            string line = dataMatrix[i][0];
            //Debug.Log(line);
            string[] splitArray = line.Split(" "[0]);
            pos[i] = new Vector3(float.Parse(splitArray[1]) * 1000.0f,
                                       float.Parse(splitArray[2]) * 100.0f + 5.0f,
                                       float.Parse(splitArray[0]) * 1000.0f);
        }

        return pos;
    }
}
