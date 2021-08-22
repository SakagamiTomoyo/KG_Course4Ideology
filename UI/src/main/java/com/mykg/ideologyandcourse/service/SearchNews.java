package com.mykg.ideologyandcourse.service;

import com.mykg.ideologyandcourse.pojo.Course;
import com.mykg.ideologyandcourse.pojo.News;
import com.mykg.ideologyandcourse.repository.CourseRepo;
import com.mykg.ideologyandcourse.repository.NewsRepo;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SearchNews {
    public List<News> search_news_by_course(NewsRepo newsRepo, String course){
        List<News> res = newsRepo.findNewsByCourse(course);
        return res;
    }

    public List<News> search_news_by_chapter(NewsRepo newsRepo, String chapter, String course){
        List<News> res = newsRepo.findNewsByChapter(chapter, course);
        return res;
    }

    public List<News> search_news_by_section(NewsRepo newsRepo, String section, String chapter, String course){
        List<News> res = newsRepo.findNewsBySection(section, chapter, course);
        return res;
    }


}
