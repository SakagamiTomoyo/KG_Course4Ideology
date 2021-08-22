package com.mykg.ideologyandcourse.pojo;

import java.util.Arrays;
import java.util.Random;
import java.util.Random.*;

class Graph_Node_ItemStyle{
    String color;
    float borderWidth;
    float[] borderType;
    float borderDashOffset;
    String borderCap;
    String borderJoin;
    float borderMiterlimit;
    float shadowBlur;
    float shadowOffsetX;
    float shadowOffsetY;
    float opacity = 1;

    public String getRgb() {
        return color;
    }

    public void setRgb(String rgb) {
        this.color = rgb;
    }

    public float getBorderWidth() {
        return borderWidth;
    }

    public void setBorderWidth(float borderWidth) {
        this.borderWidth = borderWidth;
    }

    public float[] getBorderType() {
        return borderType;
    }

    public void setBorderType(float[] borderType) {
        this.borderType = borderType;
    }

    public float getBorderDashOffset() {
        return borderDashOffset;
    }

    public void setBorderDashOffset(float borderDashOffset) {
        this.borderDashOffset = borderDashOffset;
    }

    public String getBorderCap() {
        return borderCap;
    }

    public void setBorderCap(String borderCap) {
        this.borderCap = borderCap;
    }

    public String getBorderJoin() {
        return borderJoin;
    }

    public void setBorderJoin(String borderJoin) {
        this.borderJoin = borderJoin;
    }

    public float getBorderMiterlimit() {
        return borderMiterlimit;
    }

    public void setBorderMiterlimit(float borderMiterlimit) {
        this.borderMiterlimit = borderMiterlimit;
    }

    public float getShadowBlur() {
        return shadowBlur;
    }

    public void setShadowBlur(float shadowBlur) {
        this.shadowBlur = shadowBlur;
    }

    public float getShadowOffsetX() {
        return shadowOffsetX;
    }

    public void setShadowOffsetX(float shadowOffsetX) {
        this.shadowOffsetX = shadowOffsetX;
    }

    public float getShadowOffsetY() {
        return shadowOffsetY;
    }

    public void setShadowOffsetY(float shadowOffsetY) {
        this.shadowOffsetY = shadowOffsetY;
    }

    public float getOpacity() {
        return opacity;
    }

    public void setOpacity(float opacity) {
        this.opacity = opacity;
    }
}

class Graph_Node_Label{
    boolean show;
    String Array;

}

public class Graph_Node {
    String name;  //id + label
    String id;
    String real_name;
    float x = new Random().nextFloat() * 1000;
    float y = new Random().nextFloat() * 1000;
    boolean fixed;
    float[] value;
    String category;
    String symbol;
    float symbolSize = 10;
    float symbolRotate;
    boolean symbolKeepAspect;
    float symbolOffset;
    Graph_Node_ItemStyle itemStyle;

    public Graph_Node(){}
    public Graph_Node(String id, String name, String type){
        this.real_name = name;
        this.id = id;
        this.category = type;
        this.name = id + "\t" + type;
    }

    @Override
    public boolean equals(Object node){
        if (node instanceof Graph_Node) {
            Graph_Node temp = (Graph_Node) node;
            return this.name.equals(temp.name);
        }
        return super.equals(node);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getReal_name() {
        return real_name;
    }

    public void setReal_name(String real_name) {
        this.real_name = real_name;
    }

    public float getX() {
        return x;
    }

    public void setX(float x) {
        this.x = x;
    }

    public float getY() {
        return y;
    }

    public void setY(float y) {
        this.y = y;
    }

    public boolean isFixed() {
        return fixed;
    }

    public void setFixed(boolean fixed) {
        this.fixed = fixed;
    }

    public float[] getValue() {
        return value;
    }

    public void setValue(float[] value) {
        this.value = value;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public float getSymbolSize() {
        return symbolSize;
    }

    public void setSymbolSize(float symbolSize) {
        this.symbolSize = symbolSize;
    }

    public float getSymbolRotate() {
        return symbolRotate;
    }

    public void setSymbolRotate(float symbolRotate) {
        this.symbolRotate = symbolRotate;
    }

    public boolean isSymbolKeepAspect() {
        return symbolKeepAspect;
    }

    public void setSymbolKeepAspect(boolean symbolKeepAspect) {
        this.symbolKeepAspect = symbolKeepAspect;
    }

    public float getSymbolOffset() {
        return symbolOffset;
    }

    public void setSymbolOffset(float symbolOffset) {
        this.symbolOffset = symbolOffset;
    }

//    public void setHighLight(boolean on_off){
//        this.itemStyle.
//    }

    public void setColor(String rgb){
        this.itemStyle.setRgb(rgb);
    }

    @Override
    public String toString() {
        return "Graph_Node{" +
                "name='" + name + '\'' +
                ", id='" + id + '\'' +
                ", real_name='" + real_name + '\'' +
                ", x=" + x +
                ", y=" + y +
                ", fixed=" + fixed +
                ", value=" + Arrays.toString(value) +
                ", category='" + category + '\'' +
                ", symbol='" + symbol + '\'' +
                ", symbolSize=" + symbolSize +
                ", symbolRotate=" + symbolRotate +
                ", symbolKeepAspect=" + symbolKeepAspect +
                ", symbolOffset=" + symbolOffset +
                '}';
    }
}
