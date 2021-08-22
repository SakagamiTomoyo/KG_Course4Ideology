package com.mykg.ideologyandcourse.service;

import com.mykg.ideologyandcourse.pojo.Course;
import com.mykg.ideologyandcourse.repository.CourseRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SearchCourse {

    public List<Course> search_course(CourseRepo courseRepo, String message){
        List<Course> courses = courseRepo.search_course(
                                "(?i).*" + message.split(":")[1]
                                        .replace("\"", "")
                                        .replace("}", "") + ".*");

        return courses;
    }
}
