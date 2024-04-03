from cube import Cube
from helper import rawCondense
from solver_data import RunePatternMatcher, movedata, move_pole_perspective, positionTransformData, whiteEdgePairs, \
    whiteEdgeDirectMoves, LyreLookUpSystem, ScythePatternMatcher, RunePatternMatcher

sequence_camera = ['CXCY', 'SNAP', 'OXCY', 'M2_R', 'CXCY', 'CXOY', 'M2M4_R', 'SNAP', 'M2M4_R', 'SNAP', 'M2M4_R', 'SNAP',
                   'M2M4_R', 'CXCY', 'OXCY', 'M2_R', 'CXCY', 'CXOY', 'M1_R', 'CXCY', 'OXCY', 'M1M3_R', 'SNAP', 'M1M3_L',
                   'M1M3_L', 'SNAP', 'M1M3_R', 'CXCY', 'CXOY', 'M1_R', 'CXCY']


# The reformat function transform the list given by the camera mapping of the cube into a list that the solving
# algorithm can take as parameter
def reformat(m):
    temp = [[['z'] * 3 for _ in range(3)] for _ in range(6)]
    m = list(m)  # Convert string to list of characters
    m = [str(element) for element in m]
    temp[0] = [[m[27], m[28], m[29]], [m[30], m[31], m[32]], [m[33], m[34], m[35]]]
    temp[1] = [[m[51], m[48], m[45]], [m[52], m[49], m[46]], [m[53], m[50], m[47]]]
    temp[2] = [[m[17], m[16], m[15]], [m[14], m[13], m[12]], [m[11], m[10], m[9]]]
    temp[3] = [[m[38], m[41], m[44]], [m[37], m[40], m[43]], [m[36], m[39], m[42]]]
    temp[4] = [[m[18], m[19], m[20]], [m[21], m[22], m[23]], [m[24], m[25], m[26]]]
    temp[5] = [[m[0], m[1], m[2]], [m[3], m[4], m[5]], [m[6], m[7], m[8]]]
    return temp





class Solver():
    """
    A Solver object that takes in a cube, solves it and gives output in the standard cube notation.

    Parameters
    ----------
    cube : Cube object
        The cube to be solved. This object will not be modified due to the solve, 
        but rather a copy is stored in the solver.

    Attributes
    ----------
    cube : Cube object
        The internal copy of the Cube object that is given.
    
    Example
    -------
    >>> cb = Cube()
    >>> cb.doMoves("RUR'U'")
    >>> solver = Solver(cb)
    >>> solver.solveCube(optimize=True)
    >>> print(solver.getMoves())
    URU'R'
    >>> print(solver.getMoves(decorated=True))
    For F2L: URU'R'
    """

    def __init__(self, cube):
        self.cube = Cube(faces=cube.getFaces())
        self.__faces = self.cube.cube
        self.__forms = []
        self.Dictio = dict(F=['M1_R'], duoF=['M1_180'], Fi=['M1_L'], duoFi=['M1_180'], R=['M4_R'], duoR=['M4_180'],
                           Ri=['M4_L'], duoRi=['M4_180'], U=['M2M4_L_F', 'M3_L', 'M2M4_R_F'],
                           duoU=['M2M4_L_F', 'M3_180', 'M2M4_R_F'], Ui=['M2M4_L_F', 'M3_R', 'M2M4_R_F'],
                           duoUi=['M2M4_L_F', 'M3_180', 'M2M4_R_F'], L=['M2_R'], duoL=['M2_180'], Li=['M2_L'],
                           duoLi=['M2_180'], B=['M3_L'], duoB=['M3_180'], Bi=['M3_R'], duoBi=['M3_180'],
                           D=['M2M4_L_F', 'M1_R', 'M2M4_R_F'], duoD=['M2M4_L_F', 'M1_180', 'M2M4_R_F'],
                           Di=['M2M4_L_F', 'M1_L', 'M2M4_R_F'], duoDi=['M2M4_L_F', 'M1_180', 'M2M4_R_F'],
                           M=['M2M4_L_B', 'M2M4_R_F'], duoM=['duoM2M4_B', 'duoM2M4_F'], Mi=['M2M4_R_B', 'M2M4_L_F'],
                           duoMi=['duoM2M4_B', 'duoM2M4_F'], E=['M1M3_L_F', 'M2M4_R_B', 'M2M4_L_F', 'M1M3_R_F'],
                           duoE=['M1M3_L_F', 'duoM2M4_B', 'duoM2M4_F', 'M1M3_R_F'],
                           Ei=['M1M3_L_F', 'M2M4_L_B', 'M2M4_R_F', 'M1M3_R_F'],
                           duoEi=['M1M3_L_F', 'duoM2M4_B', 'duoM2M4_F', 'M1M3_R_F'], S=['M1M3_L_B', 'M1M3_R_F'],
                           duoS=['duoM1M3_B', 'duoM1M3_F'], Si=['M1M3_R_B', 'M1M3_L_F'],
                           duoSi=['duoM1M3_B', 'duoM1M3_F'], f=['M3_L', 'M1M3_R_F'], fi=['M3_R', 'M1M3_L_F'],
                           r=['M2_R', 'M2M4_L_F'], ri=['M2_L', 'M2M4_R_F'],
                           u=['M2M4_L_F', 'M1_R', 'M1M3_L_F', 'M2M4_R_F'],
                           ui=['M2M4_L_F', 'M1_L', 'M1M3_R_F', 'M2M4_R_F'],
                           l=['M4_R', 'M2M4_R_F'], li=['M4_L', 'M2M4_L_F'],
                           b=['M1_R', 'M1M3_L_F'], bi=['M1_L', 'M1M3_R_F'],
                           d=['M2M4_L_F', 'M3_L', 'M1M3_R_F', 'M2M4_R_F'],
                           di=['M2M4_L_F', 'M3_R', 'M1M3_L_F', 'M2M4_R_F'], X=['M2M4_L_F'], Xi=['M2M4_R_F'],
                           Y=['M2M4_R_F', 'M1M3_R_F', 'M2M4_L_F'], Yi=['M1M3_L_F', 'M2M4_L_F', 'M1M3_R_F'],
                           Z=['M1M3_R_F'], Zi=['M1M3_L_F'], duoX=['duoM2M4_F'],
                           duoY=['M1M3_L_F', 'duoM2M4_F', 'M1M3_R_F'], duoZ=['duoM1M3_F'])
        self.servo = dict(Start=['HOME_ALL', 'CXCY'], M1_R=['CXCY', 'M1_R', 'CXOY', 'M1_L'],
                          M1_L=['CXCY', 'M1_L', 'CXOY', 'M1_R'], M2_R=['CXCY', 'M2_R', 'OXCY', 'M2_L'],
                          M2_L=['CXCY', 'M2_L', 'OXCY', 'M2_R'], M3_R=['CXCY', 'M3_R', 'CXOY', 'M3_L'],
                          M3_L=['CXCY', 'M3_L', 'CXOY', 'M3_R'], M4_R=['CXCY', 'M4_R', 'OXCY', 'M4_L'],
                          M4_L=['CXCY', 'M4_L', 'OXCY', 'M4_R'], M1_180=['CXCY', 'M1_R', 'M1_R'],
                          M2_180=['CXCY', 'M2_R', 'M2_R'], M3_180=['CXCY', 'M3_R', 'M3_R'],
                          M4_180=['CXCY', 'M4_R', 'M4_R'],
                          M1M3_R_F=['CXCY', 'CXOY', 'M3_R', 'CXCY', 'OXCY', 'M1M3_R', 'CXCY', 'CXOY', 'M1_R'],
                          M1M3_L_F=['CXCY', 'CXOY', 'M3_R', 'CXCY', 'OXCY', 'M1M3_L', 'CXCY', 'CXOY', 'M1_R'],
                          duoM1M3_F=['CXCY', 'CXOY', 'M3_R', 'CXCY', 'OXCY', 'M1M3_R', 'M1M3_R', 'CXCY', 'CXOY',
                                     'M3_R'],
                          M1M3_R_B=['CXCY', 'M1M3_R', 'CXOY', 'M1M3_R'], M1M3_L_B=['CXCY', 'M1M3_L', 'CXOY', 'M1M3_R'],
                          duoM1M3_B=['CXCY', 'M1M3_R', 'M1M3_R'],
                          M2M4_R_F=['CXCY', 'OXCY', 'M4_R', 'CXCY', 'CXOY', 'M2M4_R', 'CXCY', 'OXCY', 'M2_R'],
                          M2M4_L_F=['CXCY', 'OXCY', 'M4_R', 'CXCY', 'CXOY', 'M2M4_L', 'CXCY', 'OXCY', 'M2_R'],
                          duoM2M4_F=['CXCY', 'OXCY', 'M4_R', 'CXCY', 'CXOY', 'M2M4_L', 'M2M4_L', 'CXCY', 'OXCY',
                                     'M4_R'],
                          M2M4_R_B=['CXCY', 'M2M4_R', 'OXCY', 'M2M4_R'], M2M4_L_B=['CXCY', 'M2M4_L', 'OXCY', 'M2M4_R'],
                          duoM2M4_B=['CXCY', 'M2M4_R', 'M2M4_R'], End=['OXOY'])
        self.sequence_motors = []

    def solveCube(self, debug=False, optimize=False):
        """
        Solves the cube object (that is stored internally in the solver object).

        Parameters
        ----------
        debug : bool, default=False
            If set to True, it wil print the cube object before and after the solve.
        optimize : bool, default=False
            If set to True, it will reduce the number of moves it takes for a solve by removing perspective move redundancy.
            Not recommended if you want to understand the nature of the solve.
            The orientation is strictly fixed during the entire solve.
        """
        # applying each part of the algorithm step by step
        # if debug is set to True, it prints the cube before and after applying the algorithm
        self.optimize = optimize
        if (debug):
            print("Before:")
            print(self.cube)
        try:
            self.__forms.append("--align--")
            self.__alignFaces()
            self.__forms.append("--base--")
            self.__baseCross()
            self.__forms.append("--first--")
            self.__firstLayer()
            self.__forms.append("--oll--")
            self.__oll()
            self.__forms.append("--pll--")
            self.__pll()
        except Exception as exception:
            print(exception.__class__.__name__ + " raised in the program (looks like something is broken...)")
        self.__checkComplete()
        if (debug):
            print("After:")
            print(self.cube)

    def getMoves(self, decorated=False):
        """
        Gives the moves taken for solving the cube.

        Parameters
        ----------
        decorated : bool, default=False
            If set to True, it gives a more detailed, decorated and condensed output.

        Returns
        -------
        moves : string
            Moves taken to solve the cube.
        """
        # get the moves that have been applied till now
        if (decorated):
            current = -1
            alignmentMoves = ""
            baseCrossMoves = ""
            firstLayerMoves = ""
            ollMoves = ""
            pllMoves = ""
            for form in self.__forms:
                if (form == "--align--"):
                    current = 0
                elif (form == "--base--"):
                    current = 1
                elif (form == "--first--"):
                    current = 2
                elif (form == "--oll--"):
                    current = 3
                elif (form == "--pll--"):
                    current = 4
                else:
                    if (current == 0):
                        alignmentMoves += form
                    elif (current == 1):
                        baseCrossMoves += form
                    elif (current == 2):
                        firstLayerMoves += form
                    elif (current == 3):
                        ollMoves += form
                    elif (current == 4):
                        pllMoves += form
            moves = ""
            if (bool(alignmentMoves)):
                moves += "For Alignment: " + rawCondense(alignmentMoves) + "\n"
            if (bool(baseCrossMoves)):
                moves += "For Cross: " + rawCondense(baseCrossMoves) + "\n"
            if (bool(firstLayerMoves)):
                moves += "For F2L: " + rawCondense(firstLayerMoves) + "\n"
            if (bool(ollMoves)):
                moves += "For OLL: " + rawCondense(ollMoves) + "\n"
            if (bool(pllMoves)):
                moves += "For PLL: " + rawCondense(pllMoves) + "\n"
            moves = moves.strip()
            return moves
        else:
            moves = ""
            for form in self.__forms:
                if (
                        form != "--align--" and form != "--base--" and form != "--first--" and form != "--oll--" and form != "--pll--"):
                    moves += form + "\n"
            moves = moves.strip()
            return moves

    def isSolved(self):
        """
        Checks if the cube is solved or not.

        Returns
        -------
        is_solved : bool
            If solved, it is True otherwise False.
        """
        is_solved = True
        for i in range(6):
            tar = self.__faces[i][0][0]
            for row in range(3):
                for col in range(3):
                    if (tar != self.__faces[i][row][col]):
                        is_solved = False
        return is_solved

    def __checkComplete(self):
        # checks the completion of the cube solve
        isDone = True
        for i in range(6):
            tar = self.__faces[i][0][0]
            for row in range(3):
                for col in range(3):
                    if (tar != self.__faces[i][row][col]):
                        isDone = False
        if (not isDone):
            print("<<<ERROR>>>")
            print("The program was not able to solve the cube")
            print("Please contact me (saiakarsh193@gmail.com) and send the scramble used in order fix it")

    def __moveMapper(self, side, form, handle_x=False):
        # flexible moves-mapper from local perspective to global perspective
        moves = []
        for ch in form:
            if (ch.isalpha() or ch.isdigit()):
                moves.append(ch)
            else:
                moves[-1] += ch
        onX = 0
        for i, item in enumerate(moves):
            if (handle_x):
                if (item == "x"):
                    onX += 1
                    moves[i] = ""
                elif (item == "x'"):
                    onX -= 1
                    moves[i] = ""
                elif (onX != 0):
                    tmp = 0 if (onX == 1) else 4
                    if moves[i] in move_pole_perspective:
                        moves[i] = move_pole_perspective[moves[i]][tmp + side]
                    continue
            if (self.optimize and item[0] == "y"):
                if (item == "y"):
                    side = (side + 1) % 4
                else:
                    side = (side - 1) % 4
                moves[i] = ""
            if moves[i] in movedata:
                moves[i] = movedata[moves[i]][side]
        return ''.join(moves)

    def __positionMapper(self, target, side, row=None, col=None):
        # position mapper that maps perspective local positions to global positions
        if (type(side) is tuple):
            row = side[1]
            col = side[2]
            side = side[0]
        aside, arow, acol = positionTransformData[target][side][row][col]
        return self.__faces[aside][arow][acol]

    def __move(self, form):
        # applying moves to the cube and then storing it in a list
        if (bool(form)):
            self.cube.doMoves(form)
            self.__forms.append(form)

    def __alignFaces(self):
        # aligns the cube such that green is facing the screen (outwards) and yellow is facing upwards
        if (self.__faces[1][1][1] == "G"):
            self.__move("y")
        elif (self.__faces[2][1][1] == "G"):
            self.__move("y2")
        elif (self.__faces[3][1][1] == "G"):
            self.__move("y'")
        elif (self.__faces[4][1][1] == "G"):
            self.__move("x")
        elif (self.__faces[5][1][1] == "G"):
            self.__move("x'")
        if (self.__faces[1][1][1] == "Y"):
            self.__move("z'")
        elif (self.__faces[4][1][1] == "Y"):
            self.__move("z2")
        elif (self.__faces[3][1][1] == "Y"):
            self.__move("z")

    def __baseCross(self):
        # G O B R
        # find best slot/orientation to use rather than forcing it to a standard orientation
        t_slot = 0
        t_score = 0
        for i in range(4):
            score = bool(self.__positionMapper(i, 0, 2, 1) == "G" and self.__positionMapper(i, 4, 0, 1) == "W") + bool(
                self.__positionMapper(i, 1, 2, 1) == "O" and self.__positionMapper(i, 4, 1, 2) == "W") + bool(
                self.__positionMapper(i, 2, 2, 1) == "B" and self.__positionMapper(i, 4, 2, 1) == "W") + bool(
                self.__positionMapper(i, 3, 2, 1) == "R" and self.__positionMapper(i, 4, 1, 0) == "W")
            if (score > t_score):
                t_slot = i
                t_score = score
        # if score is 4 then all the white edges are correctly oriented but may not be properly aligned
        if (t_score == 4):
            if (t_slot == 1):
                self.__move("D'")
            elif (t_slot == 2):
                self.__move("D2")
            elif (t_slot == 3):
                self.__move("D")
            return
        #  0
        # 3 1
        #  2
        # find the color slot using the best parent (green as reference) slot
        slotToColorMap = {"G": (0 + t_slot) % 4, "O": (1 + t_slot) % 4, "B": (2 + t_slot) % 4, "R": (3 + t_slot) % 4}
        # global slot to local perspective
        slot_to_persp = [[0, 1, 2, 3], [3, 0, 1, 2], [2, 3, 0, 1], [1, 2, 3, 0]]
        possible_moves = []
        # find all the edges and calculate the moves
        for persp in range(4):
            for pos in whiteEdgePairs.keys():
                if (self.__positionMapper(persp, pos) == "W"):
                    # find the other color on this edge
                    target_other = whiteEdgePairs[pos]
                    target_other_color = self.__positionMapper(persp, target_other)
                    # color to global slot
                    g_slot = slotToColorMap[target_other_color]
                    # global slot to perspective slot
                    p_slot = slot_to_persp[persp][g_slot]
                    # edge move for pos in perspective to perspective slot (as good as the global)
                    edgeMove = whiteEdgeDirectMoves[pos][p_slot]
                    # apply perspective edge move globally
                    possible_moves.append(self.__moveMapper(persp, edgeMove))
        if (len(possible_moves) > 0):
            # find the smallest move and apply it
            smallest_move = ""
            for move in possible_moves:
                if (len(move) < len(smallest_move) or smallest_move == ""):
                    smallest_move = move
            self.__move(smallest_move)
        else:
            # if no edge is found, then the miss-oriented edges are on the white face. So we check wrt the global slot
            #  which edge is out of alignment and move it out of the white face
            if (self.__positionMapper(t_slot, 0, 2, 1) != "G"):
                self.__move(self.__moveMapper(t_slot, "F2"))
            elif (self.__positionMapper(t_slot, 1, 2, 1) != "O"):
                self.__move(self.__moveMapper(t_slot, "R2"))
            elif (self.__positionMapper(t_slot, 2, 2, 1) != "B"):
                self.__move(self.__moveMapper(t_slot, "B2"))
            else:
                self.__move(self.__moveMapper(t_slot, "L2"))
        # repeatedly call this function till all the edges are oriented correctly
        self.__baseCross()

    def __getf2lMove(self, section, attrib_corner, attrib_edge, attrib_dist_sign=None, attrib_dist=None):
        # searches the dictionary and retrieves the move if found
        for f2lmove in LyreLookUpSystem["f2ldb"]:
            if (f2lmove[0] == section):
                if (section == "1a" and f2lmove[1] == attrib_corner and f2lmove[2] == attrib_edge and f2lmove[
                    3] == attrib_dist_sign and f2lmove[4] == attrib_dist):
                    return f2lmove[5]
                if ((section == "1b1" or section == "1b2") and f2lmove[1] == attrib_corner and f2lmove[
                    2] == attrib_edge):
                    return f2lmove[3]
        return ""

    def __getCornerDetailBreakdown(self, c0, c1, c2):
        # standard corner details breakdown for finding attributes
        if (c0 == "W"):
            cx = 0
            e0 = c1
            e1 = c2
        elif (c1 == "W"):
            cx = 1
            e0 = c0
            e1 = c2
        else:
            cx = 2
            e0 = c0
            e1 = c1
        if ((e0 == "G" and e1 == "O") or (e0 == "O" and e1 == "G")):
            face2 = 0
        elif ((e0 == "O" and e1 == "B") or (e0 == "B" and e1 == "O")):
            face2 = 1
        elif ((e0 == "B" and e1 == "R") or (e0 == "R" and e1 == "B")):
            face2 = 2
        else:
            face2 = 3
        return cx, e0, e1, face2

    def __firstLayer(self):
        # conditions to check f2l completion
        con1 = (self.__faces[0][1][0] == self.__faces[0][1][1] and self.__faces[0][1][1] == self.__faces[0][1][2] and
                self.__faces[1][1][0] == self.__faces[1][1][1] and self.__faces[1][1][1] == self.__faces[1][1][2] and
                self.__faces[2][1][0] == self.__faces[2][1][1] and self.__faces[2][1][1] == self.__faces[2][1][2] and
                self.__faces[3][1][0] == self.__faces[3][1][1] and self.__faces[3][1][1] == self.__faces[3][1][2])
        con2 = (self.__faces[0][2][0] == self.__faces[0][2][1] and self.__faces[0][2][1] == self.__faces[0][2][2] and
                self.__faces[1][2][0] == self.__faces[1][2][1] and self.__faces[1][2][1] == self.__faces[1][2][2] and
                self.__faces[2][2][0] == self.__faces[2][2][1] and self.__faces[2][2][1] == self.__faces[2][2][2] and
                self.__faces[3][2][0] == self.__faces[3][2][1] and self.__faces[3][2][1] == self.__faces[3][2][2])
        con3 = (self.__faces[0][1][1] == self.__faces[0][2][1] and self.__faces[1][1][1] == self.__faces[1][2][1] and
                self.__faces[2][1][1] == self.__faces[2][2][1] and self.__faces[3][1][1] == self.__faces[3][2][1])
        con4 = (self.__faces[4][1][1] == self.__faces[4][0][0] and self.__faces[4][1][1] == self.__faces[4][0][2] and
                self.__faces[4][1][1] == self.__faces[4][2][0] and self.__faces[4][1][1] == self.__faces[4][2][2])
        if (con1 and con2 and con3 and con4):
            return
        found = False
        # f2l 1a
        # trying to find a corner-edge pair
        for corner in LyreLookUpSystem["corners"]:
            c0 = self.__positionMapper(0, corner[0])
            c1 = self.__positionMapper(0, corner[1])
            c2 = self.__positionMapper(0, corner[2])
            if (c0 == "W" or c1 == "W" or c2 == "W"):
                cx, e0, e1, face2 = self.__getCornerDetailBreakdown(c0, c1, c2)
                # orienting the corner and front face properly
                face2_to_corner = [5, 3, 1, 7]
                diff = int((face2_to_corner[face2] - corner[3]) / 2) % 4
                diff_to_move = {0: "", 1: "U", 2: "U2", 3: "U'"}
                orient_move = [["", ""], ["y", "y'"], ["y2", "y2"], ["y'", "y"]]
                # top row edges
                for edge in LyreLookUpSystem["edges"]:
                    te0 = self.__positionMapper(0, edge[0])
                    te1 = self.__positionMapper(0, edge[1])
                    if ((te0 == e0 and te1 == e1) or (te0 == e1 and te1 == e0)):
                        # found a corner-edge pair
                        # attrib_corner: U means up, L means left, R means right
                        attrib_corner = "U" if (corner[cx][0] == 5) else ("L" if corner[cx][2] == 0 else "R")
                        attrib_edge = ""
                        if (edge[0][0] == 5):
                            top_col_edge = te0
                        else:
                            top_col_edge = te1
                        # attrib_edge: E means same colors, X mean not same colors
                        if (attrib_corner != "U"):
                            if (c0 != "W" and corner[0][0] == 5):
                                top_col_cor = c0
                            elif (c1 != "W" and corner[1][0] == 5):
                                top_col_cor = c1
                            else:
                                top_col_cor = c2
                            attrib_edge = "E" if (top_col_edge == top_col_cor) else "X"
                        else:
                            if (c0 != "W" and corner[0][2] == 0):
                                left_col_cor = c0
                            elif (c1 != "W" and corner[1][2] == 0):
                                left_col_cor = c1
                            else:
                                left_col_cor = c2
                            attrib_edge = "E" if (top_col_edge == left_col_cor) else "X"
                        # attrib_dist: manhattan distance between edge and corner
                        # attrib_dist_sign: 1 means clockwise corner to edge, 0 means anti-clockwise
                        if (edge[2] >= corner[3]):
                            attrib_dist = edge[2] - corner[3]
                            if (8 - attrib_dist < attrib_dist):
                                attrib_dist = 8 - attrib_dist
                                attrib_dist_sign = 0
                            else:
                                attrib_dist_sign = 1
                        else:
                            attrib_dist = corner[3] - edge[2]
                            if (8 - attrib_dist < attrib_dist):
                                attrib_dist = 8 - attrib_dist
                                attrib_dist_sign = 1
                            else:
                                attrib_dist_sign = 0
                        if (self.optimize):
                            self.__move(self.__moveMapper(face2,
                                                          diff_to_move[diff] + self.__getf2lMove("1a", attrib_corner,
                                                                                                 attrib_edge,
                                                                                                 attrib_dist_sign,
                                                                                                 attrib_dist)))
                        else:
                            self.__move(diff_to_move[diff])
                            self.__move(orient_move[face2][0])
                            self.__move(
                                self.__getf2lMove("1a", attrib_corner, attrib_edge, attrib_dist_sign, attrib_dist))
                            self.__move(orient_move[face2][1])
                        found = True
                        break
            if (found):
                break
        # f2l 1b1
        if (not found):
            # trying to find a corner-edge pair
            for corner in LyreLookUpSystem["corners"]:
                c0 = self.__positionMapper(0, corner[0])
                c1 = self.__positionMapper(0, corner[1])
                c2 = self.__positionMapper(0, corner[2])
                if (c0 == "W" or c1 == "W" or c2 == "W"):
                    cx, e0, e1, face2 = self.__getCornerDetailBreakdown(c0, c1, c2)
                    # orienting the corner and front face properly
                    face2_to_corner = [5, 3, 1, 7]
                    diff = int((face2_to_corner[face2] - corner[3]) / 2) % 4
                    diff_to_move = {0: "", 1: "U", 2: "U2", 3: "U'"}
                    orient_move = [["", ""], ["y", "y'"], ["y2", "y2"], ["y'", "y"]]
                    # middle row edges
                    for edge in LyreLookUpSystem["edges-mid"]:
                        te0 = self.__positionMapper(0, edge[0])
                        te1 = self.__positionMapper(0, edge[1])
                        if (((te0 == e0 and te1 == e1) or (te0 == e1 and te1 == e0)) and (
                                (te0 == self.__faces[edge[0][0]][1][1] and te1 == self.__faces[edge[1][0]][1][1]) or (
                                te0 == self.__faces[edge[1][0]][1][1] and te1 == self.__faces[edge[0][0]][1][1]))):
                            attrib_corner = "U" if (corner[cx][0] == 5) else ("L" if corner[cx][2] == 0 else "R")
                            attrib_edge = "E" if (
                                    te0 == self.__faces[edge[0][0]][1][1] and te1 == self.__faces[edge[1][0]][1][
                                1]) else "X"
                            if (self.optimize):
                                self.__move(self.__moveMapper(face2, diff_to_move[diff] + self.__getf2lMove("1b1",
                                                                                                            attrib_corner,
                                                                                                            attrib_edge)))
                            else:
                                self.__move(diff_to_move[diff])
                                self.__move(orient_move[face2][0])
                                self.__move(self.__getf2lMove("1b1", attrib_corner, attrib_edge))
                                self.__move(orient_move[face2][1])
                            found = True
                            break
                if (found):
                    break
        # f2l 1b2
        if (not found):
            # trying to find a corner-edge pair
            for corner in LyreLookUpSystem["corners-down"]:
                c0 = self.__positionMapper(0, corner[0])
                c1 = self.__positionMapper(0, corner[1])
                c2 = self.__positionMapper(0, corner[2])
                if (self.__faces[corner[0][0]][1][1] in [c0, c1, c2] and self.__faces[corner[1][0]][1][1] in [c0, c1,
                                                                                                              c2] and
                        self.__faces[corner[2][0]][1][1] in [c0, c1, c2]):
                    cx, e0, e1, face2 = self.__getCornerDetailBreakdown(c0, c1, c2)
                    if (self.__faces[face2][1][1] == self.__faces[face2][1][2] and self.__faces[(face2 + 1) % 4][1][
                        0] == self.__faces[(face2 + 1) % 4][1][1]):
                        continue
                    # orienting the corner and front face properly
                    orient_move = [["", ""], ["y", "y'"], ["y2", "y2"], ["y'", "y"]]
                    # # top row edges
                    for edge in LyreLookUpSystem["edges"]:
                        te0 = self.__positionMapper(0, edge[0])
                        te1 = self.__positionMapper(0, edge[1])
                        if ((te0 == e0 and te1 == e1) or (te0 == e1 and te1 == e0)):
                            down_color, down_face = (te0, edge[0][0]) if (edge[0][0] != 5) else (te1, edge[1][0])
                            color_to_face2 = {"G": 0, "O": 1, "B": 2, "R": 3}
                            diff = down_face - color_to_face2[down_color]
                            diff_to_move = {0: "", 1: "U", 2: "U2", 3: "U'", -1: "U'", -2: "U2", -3: "U"}
                            rl_map_face2 = [[0, 1], [1, 2], [2, 3], [3, 0]]
                            attrib_corner = "D" if (corner[cx][0] == 4) else ("L" if corner[cx][2] == 0 else "R")
                            attrib_edge = "L" if (rl_map_face2[face2][0] == color_to_face2[down_color]) else "R"
                            if (self.optimize):
                                self.__move(self.__moveMapper(face2, diff_to_move[diff] + self.__getf2lMove("1b2",
                                                                                                            attrib_corner,
                                                                                                            attrib_edge)))
                            else:
                                self.__move(orient_move[face2][0])
                                self.__move(diff_to_move[diff])
                                self.__move(self.__getf2lMove("1b2", attrib_corner, attrib_edge))
                                self.__move(orient_move[face2][1])
                            found = True
                            break
                if (found):
                    break
        # non standard cases
        if (not found):
            # if no possible standard case is found, then the corners and edges need to be moved around
            # so we move the unsolved corners using a score system, which rates the shorter moves and moves which form pairs with higher score
            fmoves = []
            for i in range(4):
                con1 = self.__positionMapper(i, 0, 1, 2) == self.__positionMapper(i, 0, 2, 2) and self.__positionMapper(
                    i, 1, 1, 0) == self.__positionMapper(i, 1, 2, 0) and self.__positionMapper(i, 4, 0, 2) == "W"
                con2 = self.__positionMapper(i, 0, 1, 1) == self.__positionMapper(i, 0, 1, 2) and self.__positionMapper(
                    i, 1, 1, 0) == self.__positionMapper(i, 1, 1, 1)
                corvd = [self.__positionMapper(i, 0, 2, 2), self.__positionMapper(i, 1, 2, 0),
                         self.__positionMapper(i, 4, 0, 2)]
                corvu = [self.__positionMapper(i, 0, 0, 2), self.__positionMapper(i, 1, 0, 0),
                         self.__positionMapper(i, 5, 2, 2)]
                if (con1 and con2):
                    continue
                if (con1 and not con2):
                    fmoves.append([10, self.__moveMapper(i, "RUR'")])
                if ("W" in corvd):
                    if (self.__positionMapper(i, 0, 0, 1) in corvd and self.__positionMapper(i, 5, 2, 1) in corvd):
                        fmoves.append([6, self.__moveMapper(i, "URU'R'")])
                    fmoves.append([4, self.__moveMapper(i, "RU'R'")])
                if ("W" in corvu):
                    if (self.__positionMapper(i, 0, 1, 2) in corvu and self.__positionMapper(i, 1, 1, 0) in corvu):
                        if (self.__positionMapper(i, 0, 0, 2) == "W"):
                            if (self.__positionMapper(i, 5, 2, 2) == self.__positionMapper(i, 0, 1, 2)):
                                fmoves.append([8, self.__moveMapper(i, "U'RU'R'")])
                            else:
                                fmoves.append([8, self.__moveMapper(i, "U2RUR'")])
                        elif (self.__positionMapper(i, 1, 0, 0) == "W"):
                            if (self.__positionMapper(i, 5, 2, 2) == self.__positionMapper(i, 0, 1, 2)):
                                fmoves.append([8, self.__moveMapper((i + 1) % 4, "U2L'U'L")])
                            else:
                                fmoves.append([8, self.__moveMapper((i + 1) % 4, "UL'UL")])
                        else:
                            if (self.__positionMapper(i, 0, 0, 2) == self.__positionMapper(i, 0, 1, 2)):
                                fmoves.append([9, self.__moveMapper(i, "RU'R'")])
                            else:
                                fmoves.append([4, self.__moveMapper(i, "U'RUR'")])
                fmoves.append([1, self.__moveMapper(i, "RU'R'")])
            fmoves = sorted(fmoves, key=lambda x: -x[0])
            self.__move(fmoves[0][1])
        self.__firstLayer()

    def __ollhash(self, values):
        # hashes and searches the dictionary and retrieves the move if found
        shash = ""
        for val in values:
            if (val == "Y"):
                shash += "y"
            else:
                shash += "x"
        shash = shash[0: 3] + "-" + shash[3: 8] + "-" + shash[8: 13] + "-" + shash[13: 18] + "-" + shash[18: 21]
        if (shash in ScythePatternMatcher):
            return ScythePatternMatcher[shash]
        else:
            return None

    def __oll(self):
        # performs orientation of last layer
        for i in range(4):
            ocols = []
            for pos in ScythePatternMatcher["target"]:
                ocols.append(self.__positionMapper(i, pos))
            form = self.__ollhash(ocols)
            if (bool(form)):
                if (self.optimize):
                    self.__move(self.__moveMapper(i, form, handle_x=True))
                else:
                    facemap = ["", "y", "y2", "y'"]
                    self.__move(facemap[i])
                    self.__move(form)
                break

    def __pllhash(self, values):
        # hashes and searches the dictionary and retrieves the move if found
        for shuffle in RunePatternMatcher['shufflemap']:
            ohash = ""
            for val in values:
                ohash += shuffle[val]
            if (ohash in RunePatternMatcher):
                return RunePatternMatcher[ohash]
        return None

    def __pll(self):
        # performs permutation of last layer
        for i in range(4):
            ocols = []
            for pos in RunePatternMatcher["target"]:
                ocols.append(self.__positionMapper(i, pos))
            form = self.__pllhash(ocols)
            if (bool(form)):
                if (self.optimize):
                    self.__move(self.__moveMapper(i, form, handle_x=True))
                else:
                    facemap = ["", "y", "y2", "y'"]
                    self.__move(facemap[i])
                    self.__move(form)
                break
        if (self.__faces[0][0][1] == self.__faces[1][1][1]):
            self.__move("U'")
        elif (self.__faces[0][0][1] == self.__faces[2][1][1]):
            self.__move("U2")
        elif (self.__faces[0][0][1] == self.__faces[3][1][1]):
            self.__move("U")

    # The 'reformat' function transform the movement list given by the solving algorithm
    # into a list that can be treated after by the motor movements dictionaries. There is
    # also a little bit of movement optimization/simplification.
    @staticmethod
    def reformat(moves_raw):
        moves_raw = (moves_raw.replace('For Alignment: ', '').replace('For Cross: ', '').replace('For F2L: ', '').
                     replace('For OLL: ', '').replace('For PLL: ', '').replace('\n', '').replace('x', 'X').
                     replace('y', 'Y').replace('z', 'Z').replace('Fw', 'f').replace('Rw', 'r').
                     replace('Uw', 'u').replace('Lw', 'l').replace('Bw', 'b').replace('Dw', 'd').replace('\'', 'i'))
        moves_list = []
        i = 0
        while i < len(moves_raw):
            if moves_raw[i] != 'i' and not moves_raw[i].isdigit():
                try:
                    if moves_raw[i + 1] != 'i':
                        moves_list.append(moves_raw[i])
                    else:
                        moves_list.append(moves_raw[i] + 'i')
                except IndexError:
                    moves_list.append(moves_raw[i])
            if moves_raw[i].isdigit():
                moves_list[len(moves_list) - 1] = '2' + moves_list[len(moves_list) - 1]
            i = i + 1
        for index, move in enumerate(moves_list):
            moves_list[index] = move.replace('2', 'duo')

        # Little movement optimization
        i = 0
        length = len(moves_list)
        while i < length:
            if moves_list[i][:3] == 'duo':
                try:
                    if moves_list[i][-1] == moves_list[i + 1]:
                        moves_list[i] = moves_list[i + 1] + 'i'
                        del moves_list[i + 1]
                        length = length - 1
                    if moves_list[i][-1] == moves_list[i + 1][0] and len(moves_list[i + 1]) == 2:
                        moves_list[i] = moves_list[i + 1][0]
                        del moves_list[i + 1]
                        length = length - 1
                except IndexError:
                    pass
            elif len(moves_list[i]) == 1:
                try:
                    if moves_list[i] == moves_list[i + 1][-1] and moves_list[i + 1][:3] == 'duo':
                        moves_list[i] = moves_list[i] + 'i'
                        del moves_list[i + 1]
                        length = length - 1
                except IndexError:
                    pass
            elif len(moves_list[i]) == 2:
                try:
                    if moves_list[i][0] == moves_list[i + 1][-1] and moves_list[i + 1][:3] == 'duo':
                        moves_list[i] = moves_list[i][0]
                        del moves_list[i + 1]
                        length = length - 1
                except IndexError:
                    pass
            i = i + 1
        return moves_list

    # The 'translate' function transforms the Rubik's moves into motors moves
    # using the dictionaries 'Dictio' and 'servo'
    def translate(self, moves):
        temp = []
        array_of_array = [[] for _ in range(len(moves))]
        array_of_array1 = [[] for _ in range(len(moves))]
        for i in range(len(moves)):
            temp.extend(self.Dictio[moves[i]])
            array_of_array[i].extend(self.Dictio[moves[i]])
        for j in range(len(temp)):
            self.sequence_motors.extend(self.servo[temp[j]])
        self.sequence_motors.extend(self.servo['End'])
        i = 0
        for array in array_of_array:
            for move in array:
                array_of_array1[i].extend(self.servo[move])
            i = i + 1
        return array_of_array1
