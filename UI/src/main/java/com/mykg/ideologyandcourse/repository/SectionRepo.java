package com.mykg.ideologyandcourse.repository;


import com.mykg.ideologyandcourse.pojo.Chapter;
import com.mykg.ideologyandcourse.pojo.Section;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface SectionRepo extends Neo4jRepository<Section, Long> {
    @Query("match(emp:Course)-[]-(n:Chapter)-[]-(m:Section)" +
            " where emp.name = $course and n.name = $chapter" +
            " return m")
    List<Section> search_section(@Param("course") String course,
                                 @Param("chapter") String chapter);

}
