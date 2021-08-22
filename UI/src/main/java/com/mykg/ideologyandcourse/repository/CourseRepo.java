package com.mykg.ideologyandcourse.repository;

import com.mykg.ideologyandcourse.pojo.Course;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CourseRepo extends Neo4jRepository<Course, Long> {
    @Query("match(c:Course) where c.name =~ ('(?i).*'+$course+'.*') return c")
//    @Query("match(c:Course) return c")
    List<Course> search_course(@Param("course") String course);
}
