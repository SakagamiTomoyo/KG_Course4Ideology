package com.mykg.ideologyandcourse.pojo;

import sun.awt.image.ImageWatched;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

class NameList {
    String name;

    NameList(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}

public class Graph_Categories {
    List<NameList> data;

    Graph_Categories(String[] namelist) {
        data = new ArrayList<>();
        for (String name : namelist) {
            data.add(new NameList(name));
        }
    }

    Graph_Categories(List<String> nameList) {
        data = new ArrayList<>();
        for (String name : nameList) {
            data.add(new NameList(name));
        }
    }

    public List<NameList> getData() {
        return data;
    }

    public List<String> getData_str(){
        List<String> res = new LinkedList<>();
        for(NameList nameList: data){
            res.add(nameList.name);
        }
        return res;
    }

    public void setData(List<NameList> data) {
        this.data = data;
    }
}
