package com.mykg.ideologyandcourse.pojo;

import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;

@Node
public class Chapter implements Comparable<Chapter>{
    @Id
    @GeneratedValue
    private Long Id;

    String id;
    String name;

    public Chapter() {
    }

    public Chapter(String id, String name) {
        this.id = id;
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public int compareTo(Chapter node){
        return Integer.parseInt(this.getId()) - Integer.parseInt(node.getId());
    }
}
