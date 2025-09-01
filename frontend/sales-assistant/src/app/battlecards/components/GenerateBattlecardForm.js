"use client";
import { useState, useEffect } from "react";
import { createBattlecard, fetchCompetitors } from "../../actions/battlecards";


export default function GenerateBattlecardForm({userId, onCreated, open, setOpen}){


    const[competitors, setCompetitors] = useState([])
    const[userCompId, setuserCompId] = useState("")
    const[title, setTitle] = useState("")


    useEffect(() =>{
        async function load() {
            if(!userId) return
            const data = await fetchCompetitors(userId)
            setCompetitors(data)
        }
        if(open) {
          load()
        } else{
          setTitle("")
          setuserCompId("")
        }  

    }, [open, userId]);


    const handleSubmit = async (e) =>{
        e.preventDefault()
        if(!title || !userCompId) return

        const newCard = await createBattlecard({
            title, 
            user_comp_id: parseInt(userCompId),
            content: "", 
            auto_release: false,
        })
        onCreated(newCard)
        setOpen(false)
        setTitle("")
        setuserCompId("")


    }


    return(

      <>


        {open && (
          <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
            {/* Animated Card */}
            <div className="bg-white/90 backdrop-blur-lg rounded-2xl p-8 w-[420px] shadow-2xl transform transition-all duration-300 scale-95 animate-fadeIn">
              <h2 className="text-2xl font-extrabold text-gray-800 mb-6 text-center">
                New Battlecard
              </h2>

              <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                {/* Input */}
                <input
                  type="text"
                  placeholder="Enter battlecard title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="border rounded-xl px-4 py-3 bg-white/70 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all"
                />

                {/* Select */}
                <select
                  value={userCompId}
                  onChange={(e) => setuserCompId(e.target.value)}
                  className="border rounded-xl px-4 py-3 bg-white/70 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all"
                >
                  <option value="">Select competitor</option>
                  {competitors.map((c) => (
                    <option key={c.user_comp_id} value={c.user_comp_id}>
                      {c.competitor.name}
                    </option>
                  ))}
                </select>

                {/* Buttons */}
                <div className="flex justify-end gap-3 mt-4">
                  <button
                    type="button"
                    onClick={() => setOpen(false)}
                    className="px-5 py-2.5 rounded-xl bg-gray-200 text-gray-700 hover:bg-gray-300 transition shadow-sm"
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    className="px-5 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 hover:scale-105 active:scale-95 transition shadow-md"
                  >
                    Save
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </>
    );

}