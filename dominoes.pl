isGoalHorizontal(CurrentState,N,Solution):-
    nth0(DominoIndex, CurrentState, 1),
    checkRightBomb(CurrentState, DominoIndex, NewValue),
    -1 \= NewValue,
    not(is_right_edge(DominoIndex,N)),
    replace(CurrentState,DominoIndex+1,1,Solution).

isGoalVertical(CurrentState,M,N,Solution):-
    nth0(DominoIndex, CurrentState, 1),
    checkDownBomb(CurrentState, DominoIndex,N, NewValue),
    -1 \= NewValue,
    not(is_bottom_edge(DominoIndex,M,N)),
    replace(CurrentState,DominoIndex+N,1,Solution).
% DFS
search(Start,M,N,Solution):-
    path([[Start,null]],[],M,N,Solution).
path([],_,_,_,Solution):-
   Solution = [], !.
   % write('No solution found').
path([[Current,Parent]|_],Closed,M,N,Solution):-
    isGoalHorizontal(Current,N,Solution),!.
   % write('A horizontal solution is found : '),
   % write(Solution), nl ,!.
path([[Current,Parent]|_],Closed,M,N,Solution):-
    isGoalVertical(Current,M,N,Solution),!.
   % write('A vertical solution is found : '),
   % write(Solution), nl ,!.
path(Open,Closed,M,N,Solution):-
    removeFromOpen(Open,[State,Parent],RestOfOpen),
    getChildren(State,Open,Closed,Children,M,N),
    append(Children,RestOfOpen,NewOpen),
    path(NewOpen,[[State,Parent]|Closed],M,N,Solution).

getChildren(State,Open,Closed,Children,M,N):-
    bagof(X, moves(State,Open,Closed,M,N,X),Children), !.
getChildren(_,_,_,[],_,_).

removeFromOpen([State|RestOfOpen],State,RestOfOpen).

%Moves
moves(State,Open,Closed,M,N,[Next,State]):-
    move(State,Next,M,N),
    \+member([Next,_],Open),
    \+member([Next,_],Closed).
move(State, Next,M,N):-
    right(State, Next,N); down(State, Next,M,N).
right(State, Next, N):-
    (
        nth0(DominoIndex, State, -1)
    ->
        nth0(DominoIndex, State, -1),
        replace(State,DominoIndex,#,NewState),
        not(is_right_edge(DominoIndex,N)),
        NewIndex is DominoIndex+1,
        checkRightBomb(NewState, DominoIndex, NewValue),
        % replace
        replace(NewState,NewIndex,NewValue,Next)
    ;
        nth0(DominoIndex, State, 1),
        not(is_right_edge(DominoIndex,N)),
        NewIndex is DominoIndex+1,
        checkRightBomb(State, DominoIndex, NewValue),
        % replace
        replace(State,NewIndex,NewValue,TempL),
        replace(TempL,DominoIndex,0,Next)
    ).
down(State, Next, M, N):-
    (
        nth0(DominoIndex, State, -1)
    ->
        nth0(DominoIndex, State, -1),
        replace(State,DominoIndex,#,NewState),
        not(is_bottom_edge(DominoIndex,M,N)),
        NewIndex is DominoIndex+N,
        checkDownBomb(NewState, DominoIndex, N, NewValue),
        % replace
        replace(NewState,NewIndex,NewValue,Next)
    ;
        nth0(DominoIndex, State, 1),
        not(is_bottom_edge(DominoIndex,M,N)),
        NewIndex is DominoIndex+N,
        checkDownBomb(State, DominoIndex, N, NewValue),
        % replace
        replace(State,NewIndex,NewValue,TempL),
        replace(TempL,DominoIndex,0,Next)
    ).

is_bottom_edge(Index,M,N) :-
    Cell is Index+1,
    Cell>=M*(N-1).

is_right_edge(Index,N) :-
    Cell is Index+1,
    0 is Cell mod N.

% NewValue is -1 if there is a right bomb else new value is 1
checkRightBomb(State, DominoIndex,NewValue):-
    RightIndex is DominoIndex+1,
    nth0(RightIndex, State, Element),
    (
        # \= Element
    ->
        NewValue = 1
    ;
        NewValue = -1
    ).

% NewValue is -1 if there is a down bomb else new value is 1
checkDownBomb(State,DominoIndex,N,NewValue):-
    DownIndex is DominoIndex+N,
    nth0(DownIndex, State, Element),
    (
        # \= Element
    ->
        NewValue = 1
    ;
        NewValue = -1
    ).


%replace indexes value while moving domino
replace([_|T], 0, X, [X|T]).
replace([H|T], Index, X, [H|R]):-
    Index > 0,
    I1 is Index-1,
    replace(T, I1, X, R).
