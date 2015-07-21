<!-- Header welcome & adds -->
<div class="row-fluid">
  <div class="span12 build-header center">

    <span>
      <p class="bold">Entrez l'url du flux rss à ajouter</p>
      <input type="text" id="board-url" data-uuid="{{ config_id }}" value="http://lehollandaisvolant.net/rss.php?mode=links">
      <button id="submit-flux" class="btn">Ajouter</button>
    </span>

    <span class="custom-url">
      <div id="custom-url" style="display:none" class="white-big"></div>
    </span>

  </div> 
</div> 

<!-- main boards list --> 
<div class="row-fluid">
  <div class="center"></div>
  <div class="span12" id="build">

    <ul id="sortable">
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-1"></span>
        <div class="board-wrapper" id="1">
          <p class="center bold slot-message">Emplacement 1</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-2"></span>
        <div class="board-wrapper" id="2">
          <p class="center bold slot-message">Emplacement 2</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-3"></span>
        <div class="board-wrapper" id="3">
          <p class="center bold slot-message">Emplacement 3</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-4"></span>
        <div class="board-wrapper" id="4">
          <p class="center bold slot-message">Emplacement 4</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-5"></span>
        <div class="board-wrapper" id="5">
          <p class="center bold slot-message">Emplacement 5</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-6"></span>
        <div class="board-wrapper" id="6">
          <p class="center bold slot-message">Emplacement 6</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-7"></span>
        <div class="board-wrapper" id="7">
          <p class="center bold slot-message">Emplacement 7</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-8"></span>
        <div class="board-wrapper" id="8">
          <p class="center bold slot-message">Emplacement 8</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-9"></span>
        <div class="board-wrapper" id="9">
          <p class="center bold slot-message">Emplacement 9</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-10"></span>
        <div class="board-wrapper" id="10">
          <p class="center bold slot-message">Emplacement 10</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-11"></span>
        <div class="board-wrapper" id="11">
          <p class="center bold slot-message">Emplacement 11</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-12"></span>
        <div class="board-wrapper" id="12">
          <p class="center bold slot-message">Emplacement 12</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-13"></span>
        <div class="board-wrapper" id="13">
          <p class="center bold slot-message">Emplacement 13</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-14"></span>
        <div class="board-wrapper" id="14">
          <p class="center bold slot-message">Emplacement 14</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-15"></span>
        <div class="board-wrapper" id="15">
          <p class="center bold slot-message">Emplacement 15</p>
        </div>
      </li>
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-16"></span>
        <div class="board-wrapper" id="16">
          <p class="center bold slot-message">Emplacement 16</p>
        </div>
      </li>
    </ul>

  </div>
</div> 


<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css"> 
<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>

%rebase base settings=settings
