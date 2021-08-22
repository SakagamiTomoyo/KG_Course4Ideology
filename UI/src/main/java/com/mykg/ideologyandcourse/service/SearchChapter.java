package com.mykg.ideologyandcourse.service;

import com.mykg.ideologyandcourse.pojo.Chapter;
import com.mykg.ideologyandcourse.pojo.Course;
import com.mykg.ideologyandcourse.repository.ChapterRepo;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SearchChapter {

    public List<Chapter> search_chapter(ChapterRepo chapterRepo, String course){
        List<Chapter> chapters = chapterRepo.search_chapter(
                course.split(":")[1].replace("\"", "").replace("}", "")
        );

        return chapters;
    }


}
