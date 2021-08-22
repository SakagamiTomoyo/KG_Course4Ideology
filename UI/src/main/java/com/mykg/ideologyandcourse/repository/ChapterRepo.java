package com.mykg.ideologyandcourse.repository;

import com.mykg.ideologyandcourse.pojo.Chapter;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ChapterRepo extends Neo4jRepository<Chapter, Long> {
    @Query("match(emp:Course)-[]-(n:Chapter) where emp.name = $course return n")
    List<Chapter> search_chapter(@Param("course") String course);
}
