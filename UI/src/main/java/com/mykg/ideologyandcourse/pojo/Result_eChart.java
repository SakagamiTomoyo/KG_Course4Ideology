package com.mykg.ideologyandcourse.pojo;

import java.util.LinkedList;
import java.util.List;

public class Result_eChart {
    List<Graph_Edge> links;
    List<Graph_Node> nodes;
    Graph_Categories categories;
    Graph_Categories legend;

    public Result_eChart(){
        links = new LinkedList<>();
        nodes = new LinkedList<>();
    }

    public void setLegend(List<String> legend){
        this.legend = new Graph_Categories(legend);
    }

    public void setCategories(List<String> categories) {
        this.categories = new Graph_Categories(categories);
    }

    public void addNode(String id, String name, String type){
        nodes.add(new Graph_Node(id, name, type));
    }

    public void addNode(Graph_Node node){
        nodes.add(node);
    }

    public void addLink(int source, int target){
        links.add(new Graph_Edge(source, target));
    }

    public void addLink(Graph_Edge edge){
        links.add(edge);
    }

    public List<Graph_Edge> getLinks() {
        return links;
    }

    public void setLinks(List<Graph_Edge> links) {
        this.links = links;
    }

    public List<Graph_Node> getNodes() {
        return nodes;
    }

    public void setNodes(List<Graph_Node> nodes) {
        this.nodes = nodes;
    }

    public Graph_Categories getCategories() {
        return categories;
    }

    public void setCategories(Graph_Categories categories) {
        this.categories = categories;
    }

    public Graph_Categories getLegend() {
        return legend;
    }

    public void setLegend(Graph_Categories legend) {
        this.legend = legend;
    }
}
