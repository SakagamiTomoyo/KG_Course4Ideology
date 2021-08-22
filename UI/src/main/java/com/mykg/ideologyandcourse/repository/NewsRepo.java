package com.mykg.ideologyandcourse.repository;

import com.mykg.ideologyandcourse.pojo.News;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface NewsRepo extends Neo4jRepository<News, Long> {
    @Query("match(n:Course)-[]-(m:News) where n.name = $course return m limit 30")
    public List<News> findNewsByCourse(@Param("course") String course);

    @Query("match(n:Chapter)-[]-(m:News) where n.name = $chapter return m limit 30")
    public List<News> findNewsByChapter(@Param("chapter") String chapter,
                                        @Param("course") String course);

    @Query("match(n:Section)-[]-(m:News) where n.name = $section return m limit 30")
    public List<News> findNewsBySection(@Param("section") String section,
                                        @Param("chapter") String chapter,
                                        @Param("course") String course);
}
