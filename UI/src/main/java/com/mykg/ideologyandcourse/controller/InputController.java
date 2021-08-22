package com.mykg.ideologyandcourse.controller;

import com.alibaba.fastjson.JSONObject;
import com.mykg.ideologyandcourse.pojo.Chapter;
import com.mykg.ideologyandcourse.pojo.Course;
import com.mykg.ideologyandcourse.pojo.News;
import com.mykg.ideologyandcourse.pojo.Section;
import com.mykg.ideologyandcourse.repository.ChapterRepo;
import com.mykg.ideologyandcourse.repository.CourseRepo;
import com.mykg.ideologyandcourse.repository.NewsRepo;
import com.mykg.ideologyandcourse.repository.SectionRepo;
import com.mykg.ideologyandcourse.service.SearchChapter;
import com.mykg.ideologyandcourse.service.SearchCourse;
import com.mykg.ideologyandcourse.service.SearchNews;
import com.mykg.ideologyandcourse.service.SearchSection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.beans.XMLEncoder;
import java.util.*;

@RestController
public class InputController {

    @Autowired
    private CourseRepo courseRepo;

    @Autowired
    private ChapterRepo chapterRepo;

    @Autowired
    private SectionRepo sectionRepo;

    @Autowired
    private NewsRepo newsRepo;

    @RequestMapping(value = "/search")
    public List<Course> getCourses(@RequestBody String message){
        SearchCourse searchCourse = new SearchCourse();
        List<Course> courses = searchCourse.search_course(courseRepo, message);
        return courses;
    }

    @RequestMapping(value = "/search_structure")
    public Map<String, List<String>> getCourseStructure(@RequestBody String message){

        Map<String, List<String>> res = new LinkedHashMap<>();

        SearchChapter searchChapter = new SearchChapter();
        SearchSection searchSection = new SearchSection();

        List<Chapter> chapters = searchChapter.search_chapter(chapterRepo, message);

        Collections.sort(chapters);
        for (Chapter chapter : chapters) {
            res.put(chapter.getName(), new LinkedList<>());
            List<Section> sections = searchSection.search_section(sectionRepo, message, chapter.getName());

            Collections.sort(sections);
            for (Section section : sections){
                res.get(chapter.getName()).add(section.getName());
            }
        }
        return res;
    }

    @RequestMapping(value = "/search_news")
    public List<News> getNews(@RequestBody String message){
        Map mes = JSONObject.parseObject(message);
        String content = (String)mes.get("content");
        String entity = (String)mes.get("entity");

        List<News> res = null;

        SearchNews searchNews = new SearchNews();

        if(entity.equals("section")){
            String chapter = (String)mes.get("father_name");
            String course = (String)mes.get("grandfather_name");
            res = searchNews.search_news_by_section(newsRepo, content, chapter, course);
        } else if(entity.equals("chapter")){
            String course = (String)mes.get("father_name");
            res = searchNews.search_news_by_chapter(newsRepo, content, course);
        } else if(entity.equals("course")){
            res = searchNews.search_news_by_course(newsRepo, content);
            System.out.println(res.size());
        }

        return res;
    }

    @RequestMapping(value = "/search_graph")
    public List<News> getGraph(@RequestBody String message){
        Map mes = JSONObject.parseObject(message);
        String content = (String)mes.get("content");
        String entity = (String)mes.get("entity");

        if(entity.equals("section")){
            String chapter = (String)mes.get("father_name");
            String course = (String)mes.get("grandfather_name");

        } else if(entity.equals("chapter")){
            String course = (String)mes.get("father_name");

        } else if(entity.equals("course")){

        }

        return null;
    }
}
