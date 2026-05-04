st.write("")
                st.markdown("#### 🛣️ Adressen")
                
                # --- OPGESPLITSTE WEERGAVE ---
                p_addr = selected_order.get('pickup_address', '-').strip()
                p_zip = selected_order.get('pickup_zip', '-').strip()
                p_city_display = selected_order.get('pickup_city', '-').strip()
                p_country = "Norway"
                
                d_addr = selected_order.get('delivery_address', '-').strip()
                d_zip = selected_order.get('delivery_zip', '-').strip()
                d_city_display = selected_order.get('delivery_city', '-').strip()
                d_country = "Norway"
                
                c_addr_left, c_addr_right = st.columns(2)
                
                with c_addr_left:
                    st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 5px;'>FROM</div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#888; font-size:12px;'>Street:</span><br><b>{p_addr}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>Zip Code & City:</span><br><b>{p_zip} {p_city_display}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>Country:</span><br><b>{p_country}</b>", unsafe_allow_html=True)

                with c_addr_right:
                    st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 5px;'>TO</div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#888; font-size:12px;'>Street:</span><br><b>{d_addr}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>Zip Code & City:</span><br><b>{d_zip} {d_city_display}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>Country:</span><br><b>{d_country}</b>", unsafe_allow_html=True)
