package com.mykg.ideologyandcourse.service;

import com.mykg.ideologyandcourse.pojo.Course;
import com.mykg.ideologyandcourse.pojo.Section;
import com.mykg.ideologyandcourse.repository.CourseRepo;
import com.mykg.ideologyandcourse.repository.SectionRepo;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SearchSection {

    public List<Section> search_section(SectionRepo sectionRepo, String message, String chapter){
        List<Section> sections = sectionRepo.search_section(
                message.split(":")[1].replace("\"", "").replace("}", ""),
                chapter);

        return sections;
    }

}
