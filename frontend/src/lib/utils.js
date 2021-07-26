/**
 * Get the first item that pass the test
 * by second argument function
 *
 * @param {Array} list
 * @param {Function} f
 * @return {*}
 */
export function find (list, f) {
  return list.filter(f)[0]
}

/**
 * Deep copy the given object considering circular structure.
 * This function caches all nested objects and its copies.
 * If it detects circular structure, use cached copy to avoid infinite loop.
 *
 * @param {*} obj ignores 支持忽略指定属性 target支持复制属性到指定对象(尽可能不构建新对象) isRemove 是否移除target中比obj多的属性
 * @param {Array<Object>} cache
 * @return {*}
 */
export function deepCopy(obj, {cache = [], ignores = [], target,isRemove = false} = {}) {
    // just return if obj is immutable value
    if (obj === null || typeof obj !== 'object') {
        return obj
    }

    // if obj is hit, it is in circular structure
    const hit = find(cache, c => c.original === obj)
    if (hit) {
        return hit.copy
    }

    const isArray = Array.isArray(obj)
    let copy = target || (isArray ? [] : {})

    if(isArray){
        //数组元素结构化复制
        let arrTarget = copy[0]
        if(arrTarget){
            //复制结构对象 保持结构原本的样子
            arrTarget = deepCopy(arrTarget,{cache, ignores})
        }
        for(let i in obj){
            if(!copy[i] && arrTarget){
                //对应位置没有目标值,复制结构对象
                copy.splice(i, 1, deepCopy(arrTarget,{cache, ignores}))
            }
            if(copy[i]){
                deepCopy(obj[i], {cache: cache,ignores: ignores,target:copy[i],isRemove: isRemove})
            }else{
                copy.push(deepCopy(obj[i], {cache, ignores}))
            }
        }
        //数组多余的项都要移除
        if(copy.length > obj.length){
            copy.splice(obj.length)
        }
    }else{
        //对象自行实现深度复制
        if(typeof obj.clone === 'function'){
            copy = obj.clone()
            // put the copy into cache at first
            // because we want to refer it in recursive deepCopy
            cache.push({
                original: obj,
                copy
            })
        }else{
            // put the copy into cache at first
            // because we want to refer it in recursive deepCopy
            cache.push({
                original: obj,
                copy
            })

            Object.keys(obj).forEach(key => {
                if (ignores.indexOf(key) < 0) {
                    //忽略属性链路处理
                    let igs = ignores.map(ig => ig.replace(new RegExp('^'+key+'\\.'),''))
                    copy[key] = deepCopy(obj[key], {cache: cache, ignores: igs,target:copy[key],isRemove: isRemove})
                }
            })

            //删除不需要的属性
            if(isRemove && typeof copy === 'object'){
                Object.keys(copy)
                    .filter(key =>obj[key] === undefined)
                    .forEach(key => delete copy[key])
            }
        }
    }

    return copy
}

/**
 * forEach for object
 */
export function forEachValue (obj, fn) {
  Object.keys(obj).forEach(key => fn(obj[key], key))
}

export function isObject (obj) {
  return obj !== null && typeof obj === 'object'
}

export function isPromise (val) {
  return val && typeof val.then === 'function'
}

export function assert (condition, msg) {
  if (!condition) throw new Error(`[vuex] ${msg}`)
}

export function partial (fn, arg) {
  return function () {
    return fn(arg)
  }
}

/**
 * 去掉字符串前后指定的字符
 * @param obj
 * @param cache 缓存
 * @param ignores 忽略的属性链
 * @param stripChars 指定去除的字符集 默认去掉空白字符
 */
export function stripObject(obj, {cache = [], ignores = [],stripChars} = {}) {
    if(!stripChars){
        stripChars = String.fromCharCode(160)+String.fromCharCode(12288)+String.fromCharCode(32)
            +String.fromCharCode(0)
    }
    // just return if obj is immutable value
    if (obj === null || typeof obj !== 'object') {
        return
    }

    // if obj is hit, it is in circular structure
    const hit = find(cache, c => c.original === obj)
    if (hit) {
        //已经去掉前后空格 直接返回,避免重复运算
        return
    }

    cache.push({
        original: obj
    })

    for(let key in obj){
        if (ignores.indexOf(key) < 0) {
            //如果当前key不在忽略列表
            if(obj[key] && obj[key].toString() === '[object File]'){
                //文件对象不处理
                continue;
            }
            const type  = typeof obj[key]
            switch(type){
                case "string":
                    let startNum = 0;
                    let endNum = 0;
                    //前空格计数
                    for (let i=0;i<obj[key].length && stripChars.indexOf(obj[key].charAt(i))>=0;i++) startNum++
                    //后空格计数
                    for (let i=obj[key].length-1;i>=0 && stripChars.indexOf(obj[key].charAt(i))>=0;i--) endNum++
                    obj[key] = obj[key].substring(startNum,obj[key].length - endNum)
                    break;
                case "object":
                    //忽略属性链路处理
                    let igs = ignores.map(ig => ig.replace(new RegExp('^'+key+'\\.'),''))
                    stripObject(obj[key],{cache,ignores:igs})
                    break;
            }
        }

    }
}

export function browserInfo() {
    let info = {};
    let ua = navigator.userAgent.toLowerCase();
    let re = /(msie|firefox|chrome|opera|version|edge|trident).*?([\d.]+)/;
    let m = ua.match(re);
    info.browser = m[1].replace(/version/, "'safari");
    info.version = m[2];
    info.number = new Number(m[2].replace(/[^\d]+/g,''));
    return info;
}
