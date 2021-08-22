package com.mykg.ideologyandcourse.pojo;

public class Graph_Edge {
    int source;
    int target;
    float value;
    String type;

    public Graph_Edge(){}
    public Graph_Edge(int source, int target) {
        this.source = source;
        this.target = target;
    }
    public Graph_Edge(int source, int target, float value) {
        this.source = source;
        this.target = target;
        this.value = value;
    }
    public Graph_Edge(int source, int target, float value, String type) {
        this.source = source;
        this.target = target;
        this.value = value;
        this.type = type;
    }



    public int getSource() {
        return source;
    }

    public void setSource(int source) {
        this.source = source;
    }

    public int getTarget() {
        return target;
    }

    public void setTarget(int target) {
        this.target = target;
    }

    public float getValue() {
        return value;
    }

    public void setValue(float value) {
        this.value = value;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
