function defineReactive(data, key, value) {
  observer(value);
  var dep = new Dep();
  Object.defineProperty(data, key, {
    get: function () {
      if (Dep.target) {
        dep.addSub(Dep.target);
      }
      return value;
    },
    set: function (newVal) {
      if (value !== newVal) {
        value = newVal;
        dep.notify();
      }
    }
  });
}

function observer(data) {
  if (!data || typeof data !== "object") {
    return;
  }
  Object.keys(data).forEach(function(key){
    defineReactive(data, key, data[key]);
  });
}

function Dep() {
  this.subs = [];
}
Dep.prototype.addSub = function (sub) {
  this.subs.push(sub);
}
Dep.prototype.notify = function () {
  for (var i = 0; i < this.subs.length; i++) {
    this.subs[i].update();
  }
}
Dep.target = null;

function Watcher(vm, prop, callback) {
  this.vm = vm;
  this.prop = prop;
  this.callback = callback;
  this.value = this.get();
}
Watcher.prototype.update = function () {
  var value = this.vm.$data[this.prop];
  var oldVal = this.value;
  if (value !== oldVal) {
    this.value = value;
    this.callback(value);
  }
}
Watcher.prototype.get = function () {
  Dep.target = this;
  var value = this.vm.$data[this.prop];
  Dep.target = null;
  return value;
}

function Compile(vm) {
  this.vm = vm;
  this.el = vm.$el;
  this.fragment = null;
  this.init();
}
Compile.prototype = {
  init: function () {
    this.fragment = this.nodeFragment(this.el);
    this.compileNode(this.fragment);
    this.el.appendChild(this.fragment);
  },
  compileNode: function (fragment) {
    var childNodes = fragment.childNodes;
    for (var i = 0; i < childNodes.length; i++) {
      var node = childNodes[i]
      if (this.isElementNode(node)) {
        this.compile(node);
      }
      if (this.isTextNode(node)){
        var reg = /\{\{(.*)\}\}/;
        var text = node.textContent;
        if (reg.test(text)) {
          var prop = reg.exec(text)[1];
          this.compileText(node, prop);
        }
      }
      if (node.childNodes && node.childNodes.length) {
        this.compileNode(node);
      }
    }
  },
  compile: function (node) {
    var nodeAttrs = node.attributes;
    for (var i = 0; i < nodeAttrs.length; i++) {
      var attr = nodeAttrs[i]
      var name = attr.name;
      if (this.isDirective(name)) {
        var value = attr.value;
        if (name === "v-model") {
          this.compileModel(node, value);
        }
      }
    }
  },
  compileModel: function (node, prop) {
    var val = this.vm.$data[prop];
    this.updateModel(node, val);
    var self = this
    new Watcher(this.vm, prop, function (value){
      self.updateModel(node, value);
    });
    node.addEventListener('input', function (e){
      var newValue = e.target.value;
      if (val === newValue) {
        return;
      }
      self.vm.$data[prop] = newValue;
    });
  },
  compileText: function (node, prop) {
    var text = this.vm.$data[prop];
    this.updateView(node, text);
    var self = this
    new Watcher(this.vm, prop, function(value) {
      self.updateView(node, value);
    });
  },
  nodeFragment: function (el) {
    var fragment = document.createDocumentFragment();
    var child = el.firstChild;
    while (child) {
      fragment.appendChild(child);
      child = el.firstChild;
    }
    return fragment;
  },
  updateModel: function(node, value) {
    node.value = typeof value == 'undefined' ? '' : value;
  },
  updateView: function (node, value) {
    node.textContent = typeof value === 'undefined' ? '' : value;
  },
  isDirective: function (attr) {
    return attr.indexOf('v-') !== -1;
  },
  isElementNode: function (node) {
    return node.nodeType === 1;
  },
  isTextNode: function (node) {
    return node.nodeType === 3;
  }
}

function Mvue(options, prop) {
  this.$options = options;
  this.$data = options.data;
  this.$prop = prop;
  this.$el = document.querySelector(options.el);
  var keys = Object.keys(this.$data)
  for (var i = 0; i < keys.length; i++) {
    this.proxyData(keys[i]);
  }
  this.init();
}
Mvue.prototype = {
  init: function () {
    observer(this.$data);
    new Compile(this);
  },
  proxyData: function (key) {
    Object.defineProperty(this, key, {
      get: function () {
        return this.$data[key]
      },
      set: function (value) {
        this.$data[key] = value;
      }
    });
  }
}