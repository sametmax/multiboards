
<!-- Header welcome & adds -->
<div class="row-fluid">
  <div class="span12 build-header center">

    <span class="white justify-left medium">
    Créez votre Multiboards,<br><br>
    Vous pouvez créer votre propre multiboards avec les sources RSS qui vous conviennent.<br>
    Tous les Boards créés sont publics.<br>
    </span>

    <span class="form-flux">
      <p class="bold">Entrez un nom pour votre Board</p>
      <input type="text" id="board-name">
      <p class="bold">Entrez l'adresse du flux RSS à ajouter</p>
      <input type="text" id="board-url" data-uuid="{{ config_id }}" value="http://sametmax.com/feed/">
      <button id="submit-flux" class="btn">Ajouter le flux RSS</button>
      <br>
      <button data-url="" id="custom-url" class="hide btn custom-url save-board bold"></button>

    </span>

  </div>
</div>

<!-- main boards list -->
<div class="row-fluid">
  <div class="center"></div>
  <div class="span12" id="build">
    <ul id="sortable">
    %for i in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']:
      <li class="build-boards span3 thumbnail board-container">
        <span class="colors-{{ i }}"></span>
        <div class="board-wrapper" id="{{ i }}">
          <p class="center bold slot-message">Emplacement {{ i }} <br><font size=1>(Glisser pour déplacer)</font></p>
        </div>
      </li>
    %end
    </ul>
  </div>
</div>


<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css">
<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
<script src="/static/js/color-thief.js"></script>

%rebase base settings=settings
