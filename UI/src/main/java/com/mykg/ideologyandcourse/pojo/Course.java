package com.mykg.ideologyandcourse.pojo;

import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;
import org.springframework.web.servlet.view.InternalResourceViewResolver;

import java.util.HashSet;
import java.util.Set;

//import org.neo4j.ogm.annotation.NodeEntity;
//import org.neo4j.ogm.annotation.Property;
//
//@NodeEntity(label = "Course")
@Node
public class Course implements Comparable<Course>{

    @Id @GeneratedValue private Long Id;

//    @Property(name = "id")
    String id;
//    @Property(name = "name")
    String name;
//    @Property(name = "link")
    String link;
//    @Property(name = "fullname")
    String fullname;

    public Course() {
    }

    public Course(String id, String name, String link, String fullname) {
        this.id = id;
        this.name = name;
        this.link = link;
        this.fullname = fullname;
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

    public String getLink() {
        return link;
    }

    public void setLink(String link) {
        this.link = link;
    }

    public String getFullname() {
        return fullname;
    }

    public void setFullname(String fullname) {
        this.fullname = fullname;
    }

//    @Relationship(type = "Chapter_Course", direction = Relationship.Direction.INCOMING)
//    public Set<Chapter> Chapter_Course;
//
//    public void addChapter(Chapter chapter) {
//        if (Chapter_Course == null) {
//            Chapter_Course = new HashSet<>();
//        }
//        Chapter_Course.add(chapter);
//    }

    @Override
    public int compareTo(Course node){
        return Integer.parseInt(this.getId()) - Integer.parseInt(node.getId());
    }

}
