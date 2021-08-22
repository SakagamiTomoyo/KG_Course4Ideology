var vm = new Vue({
    el: "#app",
    data: function(){
        return{
            keyword: '',
            left_title: '',
        }
    },
    methods: {
        search_news: function (name, entity_type, father, grandfather, event){
            axios({
                method: 'post',
                url: '/search_news',
                data: {
                    content: name,
                    father_name: father,
                    grandfather_name: grandfather,
                    entity: entity_type
                }
            }).then(function (response) {
                let doc = document.getElementById('doc-mid');
                doc.innerHTML = '';
                for(let i = 0; i < response.data.length; i++){
                    let tag = document.createElement('a');
                    tag.innerText = response.data[i].title;
                    tag.href = response.data[i].url;
                    tag.target = '_blank'
                    doc.appendChild(tag);
                    doc.appendChild(document.createElement('br'))
                }
            }).catch(function (error) {
                console.log(error);
            });
        },

        search_person: function (course_name, event){

        },

        show_graph: function (name, entity_type, father, grandfather, event){
            axios({
                method: 'post',
                url: '/search_graph',
                data: {
                    content: name,
                    father_name: father,
                    grandfather_name: grandfather,
                    entity: entity_type
                }
            }).then(function (response) {
                console.log(response)
            }).catch(function (error) {
                console.log(error);
            });
        },

        show_structure: function (course_name, event){
            axios({
                method: 'post',
                url: '/search_structure',
                data: {
                    content: course_name,
                }
            }).then(function (response) {
                let doc = document.getElementById('doc-left');
                doc.innerHTML = "";

                let h3 = document.createElement('h3');
                let a_h3 = document.createElement('a');
                a_h3.innerText = course_name;
                a_h3.href = '#';
                a_h3.onclick = function () {
                    vm.search_news(course_name, 'course', null, null);
                }
                h3.appendChild(a_h3);
                doc.appendChild(h3);

                let ul = document.createElement('ul');
                for(let item in response.data){
                    let li = document.createElement('li');
                    let a = document.createElement('a');
                    a.innerText = item;
                    a.href = '#';
                    a.onclick = function (){
                        vm.search_news(item, 'chapter', course_name, null);
                        vm.show_graph(item, 'chapter', course_name, null);
                    }
                    li.appendChild(a);
                    let ul_small = document.createElement('ul');

                    for(let i = 0; i < response.data[item].length; i++){
                        let li_small = document.createElement('li');
                        let a_small = document.createElement('a');
                        a_small.innerText = response.data[item][i];
                        a_small.href = '#';
                        a_small.onclick = function (){
                            vm.search_news(response.data[item][i], 'section', item, course_name);
                            vm.show_graph(response.data[item][i], 'section', item, course_name);
                        }
                        li_small.appendChild(a_small);
                        ul_small.appendChild(li_small);
                    }
                    li.appendChild(ul_small);
                    ul.appendChild(li);
                }
                doc.appendChild(ul);
            }).catch(function (error) {
                console.log(error);
            });
        },

        search_stock: function (course_name, event){
            vm.show_structure(course_name);
            vm.show_graph(course_name, 'course', null, null);
        },

        search_content: function (event){
            // console.log(this.keyword)
            axios({
                method: 'post',
                url: '/search',
                data: {
                    content: this.keyword,
                }
            }).then(function (response) {
                vm.left_title = '课程列表';
                let doc = document.getElementById('doc-top');
                doc.innerHTML = "";
                for(let i = 0; i < response.data.length; i++){
                    let tag = document.createElement('a');
                    tag.innerText = response.data[i].name;
                    tag.href = '#'
                    tag.onclick = function (){
                        vm.search_stock(tag.innerText)
                    }
                    doc.appendChild(tag);
                    doc.appendChild(document.createElement('br'))
                }
            }).catch(function (error) {
                console.log(error);
            });
        }
    }
})

function test_with_les_miserable(myChart){
    var option;
    myChart.showLoading();
    $.getJSON('/static/others/les-miserables.json', function (graph) {
        myChart.hideLoading();
        graph.nodes.forEach(function (node) {
            node.label = {
                show: node.symbolSize > 30
            };
        });
        option = {
            title: {
                text: 'Les Miserables',
                subtext: 'Default layout',
                top: 'bottom',
                left: 'right'
            },
            legend: [{
                data: graph.categories.map(function (a) {
                    return a.name;
                })
            }],
            animationDuration: 1500,
            animationEasingUpdate: 'quinticInOut',
            series: [
                {
                    type: 'graph',
                    layout: 'none',
                    data: graph.nodes,
                    links: graph.links,
                    categories: graph.categories,
                    roam: true,
                    label: {
                        position: 'right',
                        formatter: '{b}'
                    },
                    lineStyle: {
                        color: 'source',
                        curveness: 0.3
                    },
                    emphasis: {
                        focus: 'adjacency',
                        lineStyle: {
                            width: 10
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    });

}
