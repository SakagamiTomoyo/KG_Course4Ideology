package com.mykg.ideologyandcourse.pojo;

public class Paper {

    String id;
    String journal;
    String time;
    String title;
    String url;
    String author;

    public Paper() {
    }

    public Paper(String id, String journal, String time, String title, String url, String author) {
        this.id = id;
        this.journal = journal;
        this.time = time;
        this.title = title;
        this.url = url;
        this.author = author;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getJournal() {
        return journal;
    }

    public void setJournal(String journal) {
        this.journal = journal;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
}
