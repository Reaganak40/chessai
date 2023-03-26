using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    internal class BoardState
    {
        private Piece[] configuration;
        private string lastMove;

        private bool whiteKingMoved;
        private bool blackKingMoved;
        private int moveNumber;
        private int turn;

        public BoardState(List<Piece> white_pieces, List<Piece> black_pieces)
        {
            this.configuration = new Piece[64];

            for (int i = 0; i < 64; i++)
            {
                this.configuration[i] = new Piece(PieceType.None, GetSquareFromIndex(i));
            }

            foreach(Piece piece in white_pieces)
            {
                this.configuration[GetIndexOfPositionArray(piece.GetSquare())] = piece;
            }

            foreach (Piece piece in black_pieces)
            {
                this.configuration[GetIndexOfPositionArray(piece.GetSquare())] = piece;
            }

            this.whiteKingMoved = false;
            this.blackKingMoved = false;
            this.moveNumber = 1;
            this.turn = 0;
        }

        public void Move(string moveNotation)
        {
            if(moveNotation.Equals("O-O"))
            {
                // castle kings side
                if (turn == 0)
                {
                    // white move
                    this.whiteKingMoved = true;
                    this.Castle(true, true);
                    return;
                    
                }
                else
                {
                    // black move
                    this.blackKingMoved = true;
                    this.Castle(false, true);
                    return;
                }
            }

            string square2 = moveNotation;
           
            if (moveNotation.Count() == 2)
            {
                // this is a pawn move
                int board_index = GetIndexOfPositionArray(square2);


                if(turn == 0)
                {
                    // white's turn
                    for(int i = 1; i <= 2; i++)
                    {
                        if (this.configuration[board_index + (i * 8)].Type == PieceType.White_Pawn)
                        {
                            string square1 = GetSquareFromIndex(board_index + (i * 8));
                            this.Move(square1, square2);
                        }
                    }
                }
                else
                {
                    // black's turn
                    for (int i = 1; i <= 2; i++)
                    {
                        if (this.configuration[board_index - (i * 8)].Type == PieceType.Black_Pawn)
                        {
                            string square1 = GetSquareFromIndex(board_index - (i * 8));
                            this.Move(square1, square2);
                        }
                    }
                }
            }
            else
            {
                string[] parts = moveNotation.Split('x');

                if (parts.Count() == 2)
                {
                    if ((int)(parts[0][0]) >= 'a' && (int)(parts[0][0]) <= 'h')
                    {
                        int board_index = GetIndexOfPositionArray(parts[1]);
                        
                        // Pawn take move
                        if (turn == 0)
                        {
                            // white's turn
                            string square1 = GetSquareFromIndex(board_index + (parts[0][0] - parts[1][0]) + 8);
                            square2 = parts[1];
                            this.Move(square1, square2);
                        }
                        else
                        {
                            // black's turn
                            string square1 = GetSquareFromIndex(board_index + (parts[0][0] - parts[1][0]) - 8);
                            square2 = parts[1];
                            this.Move(square1, square2);
                        }
                    }
                    else
                    {
                        // Determine what piece 
                        int piece_index = -1;
                        switch (parts[0][0])
                        {
                            case 'Q':
                                if (turn == 0)
                                {
                                    piece_index = LocateIndexOfPiece(PieceType.White_Queen);
                                }
                                else
                                {
                                    piece_index = LocateIndexOfPiece(PieceType.Black_Queen);
                                }
                                break;
                            case 'B':
                                this.Move(parts[0] + parts[1]); // call like moving to that square and return
                                return;
                        }
                        string square1 = GetSquareFromIndex(piece_index);
                        square2 = parts[1];

                       this.Move(square1, square2);
                    }
                }
                else
                {
                    // Piece move (no take)

                    int piece_index = -1;
                    square2 = moveNotation.Substring(1);
                    switch (moveNotation[0])
                    {
                        case 'Q':
                            if (turn == 0)
                            {
                                piece_index = LocateIndexOfPiece(PieceType.White_Queen);
                            }
                            else
                            {
                                piece_index = LocateIndexOfPiece(PieceType.Black_Queen);
                            }
                            break;
                        case 'N':
                            if (turn == 0)
                            {
                                piece_index = LocateIndexOfPiece(PieceType.White_Knight, can_see : GetIndexOfPositionArray(square2));
                            }
                            else
                            {
                                piece_index = LocateIndexOfPiece(PieceType.Black_Knight, can_see: GetIndexOfPositionArray(square2));
                            }
                            break;
                        case 'B':
                            if (turn == 0)
                            {
                                piece_index = LocateIndexOfPiece(PieceType.White_Bishop, can_see: GetIndexOfPositionArray(square2));
                            }
                            else
                            {
                                piece_index = LocateIndexOfPiece(PieceType.Black_Bishop, can_see: GetIndexOfPositionArray(square2));
                            }
                            break;
                    }

                    string square1 = GetSquareFromIndex(piece_index);
                    this.Move(square1, square2);
                }
            }
        }

        public void Move(string square1, string square2)
        {
            int from = GetIndexOfPositionArray(square1);
            int to = GetIndexOfPositionArray(square2);

            this.configuration[to].SetPiece(this.configuration[from].Type);
            this.configuration[from].SetPiece(PieceType.None);

            if (this.turn == 1)
            {
                this.moveNumber++;
                this.turn = 0;
            }
            else
            {
                this.turn = 1;
            }
        }

        public void Castle(bool WhiteKing, bool right)
        {
            if (WhiteKing)
            {
                if (right)
                {
                    this.configuration[62].SetPiece(PieceType.White_King);
                    this.configuration[60].SetPiece(PieceType.None);

                    this.configuration[61].SetPiece(PieceType.White_Rook);
                    this.configuration[63].SetPiece(PieceType.None);
                }
                else
                {
                    this.configuration[58].SetPiece(PieceType.White_King);
                    this.configuration[60].SetPiece(PieceType.None);

                    this.configuration[59].SetPiece(PieceType.White_Rook);
                    this.configuration[56].SetPiece(PieceType.None);
                }
            }
            else
            {
                if (right)
                {
                    this.configuration[6].SetPiece(PieceType.Black_King);
                    this.configuration[4].SetPiece(PieceType.None);

                    this.configuration[5].SetPiece(PieceType.Black_Rook);
                    this.configuration[7].SetPiece(PieceType.None);
                }
                else
                {
                    this.configuration[6].SetPiece(PieceType.Black_King);
                    this.configuration[1].SetPiece(PieceType.None);

                    this.configuration[3].SetPiece(PieceType.Black_Rook);
                    this.configuration[0].SetPiece(PieceType.None);
                }
            }

            if (this.turn == 1)
            {
                this.moveNumber++;
                this.turn = 0;
            }
            else
            {
                this.turn = 1;
            }
        }

        private int LocateIndexOfPiece(PieceType target, int can_see = -1)
        {
            for (int i = 0; i < 64; i++)
            {
                if (this.configuration[i].Type == target)
                {
                    if (can_see < 0)
                    {
                        return i;
                    }

                    if (target == PieceType.Black_Knight || target == PieceType.White_Knight)
                    {
                        // Down 2, Right 1
                        if (((i + 17) < 64) && (((i + 17) % 8) > 0))
                        {
                            if ((i + 17) == can_see)
                            {
                                return i;
                            }
                        }

                        // Down 2, Left 1
                        if (((i + 15) < 64) && ((i + 15) % 8) < 7)
                        {
                            if ((i + 15) == can_see)
                            {
                                return i;
                            }
                        }

                        // Down 1, Right 2
                        if (((i + 10) < 64) && (((i + 10) % 8) > 1))
                        {
                            if ((i + 10) == can_see)
                            {
                                return i;
                            }
                        }

                        // Down 1, Left 2
                        if (((i + 6) < 64) && ((i + 6) % 8) < 6)
                        {
                            if ((i + 6) == can_see)
                            {
                                return i;
                            }
                        }

                        // Up 2, Right 1
                        if (((i - 15) >= 0) && (((i - 15) % 8) > 0))
                        {
                            if ((i - 15) == can_see)
                            {
                                return i;
                            }
                        }

                        // Up 2, Left 1
                        if (((i - 17) >= 0) && ((i - 17) % 8) < 7)
                        {
                            if ((i - 17) == can_see)
                            {
                                return i;
                            }
                        }

                        // Up 1, Right 2
                        if (((i - 6) >= 0) && (((i - 6) % 8) > 1))
                        {
                            if ((i - 6) == can_see)
                            {
                                return i;
                            }
                        }

                        // Up 1, Left 2
                        if (((i - 10) >= 0) && ((i - 10) % 8) < 6)
                        {
                            if ((i - 10) == can_see)
                            {
                                return i;
                            }
                        }
                    }
                    else if (target == PieceType.White_Bishop || target == PieceType.Black_Bishop)
                    {
                        if (this.IsWhiteSquare(i) == this.IsWhiteSquare(can_see))
                        {
                            return i;
                        }
                    }
                }
            }

            return -1;
        }

        private bool IsWhiteSquare(int index)
        {
            if ((index / 8) % 2 == 0)
            {
                return (index % 2 == 0);
            }
            else
            {
                return (index % 2 == 1);
            }
        }

        public bool WhiteTurn
        {
            get
            {
                return this.moveNumber % 2 == 0;
            }
        }

        private string PieceSymbol(PieceType type)
        {
            switch (type)
            {
                case PieceType.White_King:
                    return "WK";
                case PieceType.White_Queen:
                    return "WQ";
                case PieceType.White_Bishop:
                    return "WB";
                case PieceType.White_Knight:
                    return "WKN";
                case PieceType.White_Rook:
                    return "WR";
                case PieceType.White_Pawn:
                    return "WP";
                case PieceType.Black_King:
                    return "BK";
                case PieceType.Black_Queen:
                    return "BQ";
                case PieceType.Black_Bishop:
                    return "BB";
                case PieceType.Black_Knight:
                    return "BKN";
                case PieceType.Black_Rook:
                    return "BR";
                case PieceType.Black_Pawn:
                    return "BP";
                default:
                    return "___";

            }
        }

        public static string GetSquareFromIndex(int index)
        {
            string res = (char)(65 + (index % 8)) + (8 - (index / 8)).ToString();
            //Debug.WriteLine(index.ToString() + ": " + res);
            return res;
        }

        public static int GetIndexOfPositionArray(string square)
        {
            if (square.Length != 2)
            {
                throw new ArgumentException(square + " must be a chessboard sqaure value.");
            }

            int res = (int)(('8' - square[1]) * 8) + (int)(char.ToUpper(square[0]) - 'A');
            //Debug.WriteLine("square [" + square + "]: " + res.ToString());
            return res;
        }

        public override string ToString()
        {
            StringBuilder ret = new StringBuilder("");

            for(int row = 0; row < 8; row++)
            {
                for (int col = 0; col < 8; col++)
                {
                    ret.Append("[");
                    string square = this.PieceSymbol(this.configuration[(row * 8) + col].Type);
                    ret.Append(square.PadRight(3));
                    ret.Append("] ");
                }
                ret.Append("\n");
            }
            return ret.ToString();
        }

        public void DrawPieces()
        {
            foreach (Piece piece in this.configuration)
            {
                if (piece.Type != PieceType.None)
                {
                    piece.Draw();
                }
            }
        }
    }
}
