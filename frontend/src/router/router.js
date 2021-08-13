import index from "@/views/layout/index"
import article from '@/views/article/index'

export default [{
    path: '/',
    component: index,
    children:[
        ]
},
    {
        path: '/article',
        name: 'article',
        component: article
    }
]
