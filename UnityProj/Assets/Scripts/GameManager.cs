using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject MH;
    public GameObject Gibbs;
    public GameObject Hive;
    public GameObject Grad;
    public GameObject Adam;
    static string[] textlist = { " Artificial Bee Colony  ",
                                 "    Gradient Descent    ",
                                 "             Adam      ",
                                 "      Gibbs Sampling     ",
                                 "   Metropolis-Hastings  "};
    string text = textlist[0];
    private GUIStyle guiStyle = new GUIStyle();

    void Start()
    {
        guiStyle.fontSize = 50;
        guiStyle.normal.textColor = Color.white;
        Deactivate();
        Hive.SetActive(true);
        Invoke("ActivateGrad", 20.0f);
    }

    void Deactivate()
    {
        MH.SetActive(false);
        Gibbs.SetActive(false);
        Grad.SetActive(false);
        Adam.SetActive(false);
        Hive.SetActive(false);
    }

    void ActivateGrad()
    {
        Hive.GetComponent<BeeHive>().Clear();
        Deactivate();
        Grad.SetActive(true);
        Invoke("ActivateAdam", 10.0f);
        text = textlist[1];
    }

    void ActivateAdam()
    {
        Grad.GetComponent<GradSpawner>().Clear();
        Deactivate();
        Adam.SetActive(true);
        Invoke("ActivateGibbs", 20.0f);
        text = textlist[2];
    }

    void ActivateGibbs()
    {
        Adam.GetComponent<AdamSpawner>().Clear();
        Deactivate();
        Gibbs.SetActive(true);
        Invoke("ActivateMH", 20.0f);
        text = textlist[3];
    }

    void ActivateMH()
    {
        Gibbs.GetComponent<GibbsMovement>().DeActivate();
        GameObject[] gs = GameObject.FindGameObjectsWithTag("Gibbs");
        for (int i = 0; i < gs.Length; i++)
        {
            Destroy(gs[i]);
        }
        Deactivate();
        MH.SetActive(true);
        text = textlist[4];
    }

    void OnGUI()
    {
        int TextWidth = 260;
        GUI.Label(new Rect(Screen.width/2 - TextWidth, Screen.height - 100, TextWidth, 50), text, guiStyle);
    }
}
