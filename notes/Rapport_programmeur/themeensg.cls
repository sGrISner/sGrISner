%Classe de document pour le thème Latex de l'ENSG
% v.1 sept. 2010, D Lercier : création
% v.2 sept. 2012, T Coupin : création fichier classe et modif.
% v.3 sept. 2016, J. Beilin, modification de la gestion de la biblio + modifs mineures 


\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{themeensg}[28/09/2016, v3.0]

\LoadClass[twoside,11pt,a4paper]{report}
%\documentclass[twoside,11pt,a4paper]{report}
\usepackage{pdfpages} 
\RequirePackage{draftwatermark} %Filigranne brouillon
\SetWatermarkText{\textsc{Brouillon}} %Filigranne brouillon
\SetWatermarkScale{0.8} %Filigranne brouillon
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern} %lissage des polices
\RequirePackage{multirow}
\RequirePackage{calc}
%\RequirePackage{slashbox}
\RequirePackage[frenchb]{babel}
%\RequirePackage[frenchb,english]{babel}
\RequirePackage{amsmath} %maths
\RequirePackage{hyperref} %Liens vers site web
\RequirePackage{lastpage} %Numerotation des pages
\RequirePackage{acronym} %Liste des sigles
\RequirePackage{graphicx,amssymb}
\RequirePackage{float}
\RequirePackage{tabularx}
\RequirePackage[left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm]{geometry}
\RequirePackage[toc,page]{appendix}
\RequirePackage[nottoc, notlof, notlot]{tocbibind}
\RequirePackage{wrapfig} %Pour enrouler le texte autour des figures
\RequirePackage{tocloft} %pour faire la liste des équations
\RequirePackage[utf8]{inputenc}   % accents dans la source
\RequirePackage{lscape} %page en mode paysage
\RequirePackage{verbatim} %pour les commentaire sur plusieurs lignes
\RequirePackage[toc,page]{appendix} %pour les annexes
\RequirePackage{ifthen} %pour le \ifthenelse
\RequirePackage[style=numeric]{biblatex}

%---En-tête et pied de page---
\RequirePackage{fancyhdr}
\pagestyle{fancy}
% with this we ensure that the chapter and section
% headings are in lowercase.
\renewcommand{\chaptermark}[1]{%
\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{%
\markright{\thesection\ #1}}
\fancyhf{} % delete current header and footer
\fancyhead[LE]{\bfseries\thepage \hspace{0.5cm} \bfseries\leftmark}
\fancyhead[RO]{\bfseries\rightmark \hspace{0.5cm} \bfseries\thepage}

\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}
\addtolength{\headheight}{0.5pt} % space for the rule
\fancypagestyle{plain}{%
\fancyhead{} % get rid of headers on plain pages
\renewcommand{\headrulewidth}{0pt} % and the line
}
%-------------------------

%---Mise en forme des titres de chapitre--- 
\makeatletter
\def\timenow{\@tempcnta\time
  \@tempcntb\@tempcnta
  \divide\@tempcntb60
  \ifnum10>\@tempcntb0\fi\number\@tempcntb
  \multiply\@tempcntb60
  \advance\@tempcnta-\@tempcntb
  :\ifnum10>\@tempcnta0\fi\number\@tempcnta}

\def\thickhrulefill{\leavevmode \leaders \hrule height 1ex \hfill \kern \z@}

\def\@makechapterhead#1{%
  \vspace*{10\p@}%
  \begin{tabular}{b{0.8\textwidth} b{0.2\textwidth} }

  \Huge{\textsc{#1}} & \rotatebox{90}{\scshape \@chapapp{}} \fontsize{80}{80}\selectfont \texttt{\thechapter} \\
  \end{tabular}    
  
    \par\nobreak
    \hrulefill
     \par\nobreak
    \vskip 50\p@
  }
\def\@makeschapterhead#1{%
  \vspace*{10\p@}%
  {\parindent \z@ 
    {\raggedleft \reset@font
      \scshape \vphantom{\@chapapp{} \thechapter}\par\nobreak}%
    \par\nobreak
    \vspace*{30\p@}
    \interlinepenalty\@M
    {\raggedright \Huge \bfseries #1}%
    \par\nobreak
    \hrulefill
    \par\nobreak
    \vskip 50\p@
  }}
\makeatother
%------------------------------------------

%---Liste des annexes au début des annexes---
\def\appendixpage{
\pagestyle{plain}
\vspace*{4cm} 
\begin{center} 
\listofannexe
\end{center} 
} 
%--------------------------------------------

%---Section et Part en page impaire---
\newcommand{\newevenpage}{
\newpage
\ifthenelse{\isodd{\thepage}}{
}{
\phantom{placeholder} % doesn't appear on page
\thispagestyle{empty} % if want no header/footer
\newpage}
}

\newcommand{\evenpart}[2][NULL]{
\newevenpage
\ifthenelse{\equal{#1}{NULL}}{
		\part{#2}
	}
	{
		\part[#1]{#2}
	}
}

\newcommand{\evenchapter}[2][NULL]{
\newevenpage
\ifthenelse{\equal{#1}{NULL}}{
		\chapter{#2}
	}
	{
		\chapter[#1]{#2}
	}


}
%-------------------------------------


%---Compteur d'annexes---
\newlistof{annexe}{ann}{Annexes}
\newcounter{annexenb}


\newcommand{\annexe}[2][NULL]{%
\ifthenelse{\equal{#1}{NULL}}{\evenchapter{#2}}{\evenchapter[#1]{#2}}

\refstepcounter{annexenb}


\ifthenelse{\equal{#1}{NULL}}{\addcontentsline{ann}{annexe}{\protect\numberline{\theannexenb} #2}\par{}}{\addcontentsline{ann}{annexe}{\protect\numberline{\theannexenb} #1}\par{}}
}

\renewcommand{\theannexenb}{\Alph{annexenb}} 
%------------------------


%-----------------------------------------------------------------
% Couverture du rapport
%----------------------------------------------------------------
% Macro d'inclusion de l'auteur et de la date
% Parameter 1 : Prénom Nom
% Parameter 2 : Date de soutenance
\newcommand{\infos}[2]{{
\begin{center}
\begin{tabular}{c}%
\textbf{#1} \\
\\
#2 \\
\end{tabular}
\\
\vspace{1cm}
\begin{small}
\begin{tabular}{c c c c}%
$\boxtimes$ Non confidentiel & $\square$ Confidentiel IGN & $\square$ Confidentiel Industrie & $\square$ Jusqu'au ... \\
\\
\\
\multicolumn{4}{c}{\textsc{Ecole Nationale des Sciences Géographiques}} \\
\multicolumn{4}{c}{6-8 Avenue Blaise Pascal - Cité Descartes - 77420 Champs-sur-Marne} \\
\multicolumn{4}{c}{Téléphone 01 64 15 31 00   Télécopie 01 64 15 31 07} \\
\end{tabular}%
\end{small}
\end{center}
}}%
%--------------------------------------------------------------------

%--------------------------------------------------------------------
% Macro d'inclusion des logos d'entreprises
% Introduit un dessin qui représente l'entreprise
% Parameter 1 : Adresse complet de l'image en jpg
% Parameter 2 : nom de l'entreprise
\newcommand{\showgraphic}[2]{{%
\large
\begin{minipage}{4.5cm}%
\begin{center}%
\includegraphics[width=3.5cm]{#1}
\\
\vspace{0.5cm}
\textsf{\large #2}
\end{center}%
\end{minipage}%
}}
%--------------------------------------------------------------------
% Macro d'inclusion de 2 entreprises
% Introduit deux entreprises aligné en haut-gauche hau}t-droite.
% Parameter 1 : Adresse complet de l'image de l'entreprise 1
% Parameter 2 : Nom de l'entreprise 1
% Parameter 3 : Adresse complet de l'image de l'entreprise 2
% Parameter 4 : Nom de l'entreprise 2
\newcommand{\enterprise}[4]{%
\begin{center}
\showgraphic{#1}{#2}
\hfill
\ifthenelse{\equal{#3}{NULL}}{\hspace*{4.5cm}}{\showgraphic{#3}{#4}}
\end{center}
}%
%--------------------------------------------------------------------
% Macro de redéfinition de maketitle
% Introduit deux entreprises aligné en haut-gauche haut-droite.
% Parameter 1 : Nom du rapport
\makeatletter
\renewcommand{\maketitle}[2]{%
\begin{center}%
\null
\vfill
#1
{\LARGE\bfseries
\rule{\textwidth}{1.5pt}\\

\@title \\

\rule{\textwidth}{1.5pt}\\
\includegraphics[height=3cm]{#2}
}
\end{center}%
\vfill
\null
}%
\makeatother
%-------------------------------------------------------------

\graphicspath{{images/}}