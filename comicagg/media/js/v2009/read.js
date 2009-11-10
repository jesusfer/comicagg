function onReadLoad() {
	updateCounters();
	initScrolling();
	initLoadImages();
}

function initLoadImages() {
	//1. actualizar los que estan dentro del viewport
	//2. sascar el primero de la lista y cargarlo
	//ir a 2
	updateViewport(false);
	lista = cdivInView;
	do {
		div = lista.shift();
		comic = comics[div.id.substring(1)];
		_loadComic(comic);
	} while (lista.length > 0);
}

function _loadComic(comic) {
	if(!comic.loaded) {
		$('reload' + comic.id).hide();
		for(i = 0; i < comic.list.length; i++) {
			unread = comic.list[i];
			image = $('imgu' + unread.unreadid);
			_loadImage(unread.url, image, comic);
		}
		if (comic.list.length == 0) {
			image = $('imgl' + comic.id);
			_loadImage(comic.last_url, image, comic);
		}
		comic.loaded = true;
	}
}

function _loadImage(url, elem, comic) {
	elem.src = url;
	elem.cid = comic.id;
}

function imageErrorHandler(elem) {
	elem.alt = "ERROR";
	elem.src = media_url + 'images/error.png';
	comics[elem.cid].error = true;
	$('reload'+elem.cid).show();
	console.log($('reload'+elem.cid).visible());
}

function updateCounters() {
	$('menuUnreadCounter').innerHTML = ' (' + unreadCounter + ')';
	$('infoUnreadCounter').innerHTML = unreadCounter;
	$('totalComicCounter').innerHTML = comicCounter;
}

function showAllComics() {
	clist = $$('.comic');
	for (i = 0; i < clist.length; i++) {
		clist[i].show();
	}
	$('showingAll').show();
	$('showingUnread').hide();
	updateViewport(true);
}

function showUnreadComics() {
	clist = $$('.comic');
	for (i = 0; i < clist.length; i++) {
		cid = clist[i].id.substring(1);
		if (!unreadComics[cid]) {
			clist[i].hide();
		}
	}
	$('showingAll').hide();
	$('showingUnread').show();
	updateViewport(true);
}

/* Scrolling things */

var sync = false;
var cdivInView = new Array();
var comicdivs = new Array();

function initScrolling() {
	window.onscroll = onScrollHandler;
	comicdivs = $$('.comic');
}

function onScrollHandler(e) {
	updateViewport(true);
}

function updateViewport(loadImages) {
	if (sync) return;
	sync = true;
	end = false;
	viewp = false;
	vmin = document.viewport.getScrollOffsets()['top'];
	vmax = vmin + document.viewport.getHeight();
	cdivInView = new Array();
	for (i = 0; i < comicdivs.length && !end; i++) {
		cdiv = comicdivs[i];
		// solo afecta a elementos visibles
		if (cdiv.visible()) {
			if (inViewport(cdiv, vmin, vmax)) {
				cdivInView.push(cdiv);
				if (loadImages) {
					// TODO cargar las imagenes
					comic = comics[cdiv.id.substring(1)];
					if(!comic) { console.log("ERROR"); console.log(cdiv.id.substring(1)); }
					_loadComic(comic);
				}
				viewp = true;
			} else { if (viewp) { end = true; } }
		}
	}
	sync = false;
}

function inViewport(cdiv, vmin, vmax) {
	emin = cdiv.cumulativeOffset()['top'];
	h = cdiv.getHeight();
	emax = emin + h;
	c1 = emin <= vmin && emax >= vmax; // sobresale del viewport
	c2 = emin >= vmin && emin <= vmax; //el borde inferior esta dentro
	c3 = emax >= vmin && emax <= vmax; //el borde superior esta dentro
	if (c1 || c2 || c3) {
		return true;
	} else {
		return false;
	}
}